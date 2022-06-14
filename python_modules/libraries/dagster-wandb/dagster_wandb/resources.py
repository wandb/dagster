import wandb

from dagster import Field, OpExecutionContext, StringSource, resource

WANDB_CLOUD_HOST: str = 'https://api.wandb.ai'

@resource(
    {
        "api_key": Field(StringSource, description="Weights & Biases API key", is_required=True),
        "host": Field(
            StringSource,
            description="The Weights & Biases host server to connect to",
            is_required=False,
            default_value=WANDB_CLOUD_HOST,
        ),
    },
    description="Resource for interacting with the wandb SDK",
)
def wandb_resource(context: OpExecutionContext) -> wandb:
    """Resource for interacting with the wandb sdk.

    Docs for the Python library can be found at: https://docs.wandb.ai/ref/python

    Args:
        context (OpExecutionContext): Execution context pass to all resources by default

    Returns:
        wandb: Authenticated wandb client

    Example:
        .. highlight:: python
        .. code-block:: python

            @op(required_resource_keys={'wandb'})
            def do_some_nlp(context):
                wandb = context.resources.wandb
                headlines = ["A", "B", "C"]
                text_table = wandb.Table(columns=["Headline", "Positive", "Negative", "Neutral"])
                for headline in headlines:
                    pos_score, neg_score, neutral_score = model(headline)
                text_table.add_data(headline, pos_score, neg_score, neutral_score)
                wandb.log({"validation_samples" : text_table})

            @job(resource_defs={'wandb': wandb_resource})
            def wandb_job():
                do_some_nlp()
    """
    wandb.login(
        key=context.resource_config["api_key"],
        host=context.resource_config["host"],
        anonymous='never',
    )
    return wandb
