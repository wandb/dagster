from dagster import job
from dagster_wandb.launch.ops import (
    wandb_launch_single_run_op,
    wandb_launch_add_op,
    wandb_launch_agent_op
)
from dagster_wandb.resources import wandb_api_resource

@job(
    resource_defs={
        "wandbapi": wandb_api_resource.configured({"api_key": "e1c1d4d30a50023c3cceaa285bf7e16e43c93760"}),
    }
)
def pipeline():
   #  wandb_launch_single_run_op()
   wandb_launch_agent_op()