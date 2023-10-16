import chainlit as cl
from chainlit.types import AskFileResponse

from image_generator_bot.config import cfg
import image_generator_bot.backend.image_generator as image_g
from image_generator_bot.log_factory import logger

def is_yes(input_msg: str) -> bool:
    return input_msg in ("yes", "y", "Yes", "Y")

@cl.on_chat_start
async def start() -> cl.Message:
    content_of_image = await ask_user_msg("Please describe the image that you want")
    while True:
        prompt = await image_g.give_prompt(content_of_image["content"])
        logger.info(prompt)
        await cl.Message(content=f"{prompt}").send()
        prompt_satisfied = await ask_user_msg("Are you satisfied with the prompt generated?")
        if is_yes(prompt_satisfied['content']):
            while True:
                
                image = await image_g.generate_advice_image(prompt)
                await cl.Message(content="Look at the image here! click the URL").send()
                await cl.Message(content=f"{image}").send()
                image_satisfied = await ask_user_msg("Are you satisfied with the image generated?")
                if is_yes(image_satisfied['content']):
                    await cl.Message(content="Thank You! Download this image", elements=image).send()
                    break
                else:
                    await cl.Message(content="I will try again").send()
                    continue
        else:
            await cl.Message(content="I will try again").send()

async def ask_user_msg(question) -> AskFileResponse:
    ans = None
    while ans == None:
        ans = await cl.AskUserMessage(
            content=f"{question}", timeout=cfg.ui_timeout
        ).send()
    return ans

    