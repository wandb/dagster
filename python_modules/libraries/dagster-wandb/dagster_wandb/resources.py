import wandb

from dagster import Field, OpExecutionContext, StringSource, resource


@resource(
    {"api_key": Field(StringSource, description="Weights & Biases API key")},
    description="Resource for interacting with the wandb SDK",
)
def wandb_resource(context: OpExecutionContext):
    wandb.login(key=context.resource_config["api_key"])
    return wandb
