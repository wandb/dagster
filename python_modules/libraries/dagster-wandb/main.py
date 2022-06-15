import os
from dagster import job
from dagster_wandb.launch.ops import (
    wandb_launch_single_run_op,
    wandb_launch_add_op
)
from dagster_wandb.resources import wandb_api_resource

@job(
    resource_defs={
        "wandbapi": wandb_api_resource.configured({"api_key": "test-key"}),
    }
)
def pipeline():
   #  wandb_launch_single_run_op()
   wandb_launch_add_op()