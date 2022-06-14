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
def wandb_resource(context: OpExecutionContext):
    wandb.login(
        key=context.resource_config["api_key"],
        host=context.resource_config["host"],
    )
    return wandb
