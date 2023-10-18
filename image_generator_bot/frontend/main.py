import chainlit as cl
from chainlit.types import AskFileResponse

from image_generator_bot.config import cfg
import image_generator_bot.backend.image_generator as image_g
from image_generator_bot.log_factory import logger
import image_generator_bot.backend.download_img as download_img
import image_generator_bot.backend.tagging_service as ts
from image_generator_bot.backend.model import ResponseTags

def is_yes(input_msg: str) -> bool:
    return input_msg in ("yes", "y", "Yes", "Y")

def answer(input_msg: str):
    response_tags: ResponseTags =  ts.sentiment_chain_factory().run(ts.prepare_sentiment_input(input_msg))
    logger.info(response_tags)
    if response_tags.is_positive:
        return "positive"
    elif response_tags.is_negative:
        return "negative"
    elif response_tags.sounds_confused:
        return "confused"
    else:
        return "did not understand"

def is_exit(input_msg: str) -> bool:
    return input_msg in ("exit", "EXIT", "Exit")



def display_image(image_path: str, alt: str):
    return f"![{alt}]({image_path})"


@cl.on_chat_start
async def start() -> cl.Message:
    content_of_image = await ask_user_msg("Please describe the image that you want")
    while True:
        prompt = await image_g.give_prompt(content_of_image["content"])
        logger.info(prompt)
        await cl.Message(content=f"{prompt}").send()
        prompt_satisfied = await ask_user_msg(
            "Are you satisfied with the prompt generated?"
        )
        if answer(prompt_satisfied["content"]) == "positive":
            while True:
                image_url = await generate_image(content_of_image, prompt)
                image_satisfied = await ask_user_msg(
                    "Are you satisfied with the image generated?"
                )
                if answer(image_satisfied['content']) == "positive":
                    download = await ask_user_msg(
                        "Thank You! Do you want Download this image?"
                    )
                    if answer(download["content"]) == "positive":
                        await download_image(image_url)
                        break
                    else:
                        await cl.Message(content="thank you").send()
                    break
                    
                elif answer(image_satisfied["content"]) == "negative":
                    await cl.Message(content="thank you").send()
                    break
                else:
                    await cl.Message(content="I will try again").send()
                    continue
            break
        elif answer(prompt_satisfied["content"]) == "negative":
            await cl.Message(content="thank you").send()
            break
        else:
            await cl.Message(content="I will try again").send()
            continue

async def download_image(image_url):
    image_name = await ask_user_msg("What do you want to name the image?")
                    
    await download_img.download_image_dalle(image_url, image_name['content'])
    await cl.Message(
                            content="Thank you, check the image in ImageDALL-E folder"
                        ).send()

async def generate_image(content_of_image, prompt):
    image_url = await image_g.generate_advice_image(prompt)
    await cl.Message(content="Look at the image here!").send()
    await cl.Message(display_image(image_url, content_of_image)).send()
    await cl.Message(content=f"{image_url}").send()
    return image_url


async def ask_user_msg(question) -> AskFileResponse:
    ans = None
    while ans == None:
        ans = await cl.AskUserMessage(
            content=f"{question}", timeout=cfg.ui_timeout
        ).send()
    return ans
