from dagster import Field, OpExecutionContext, StringSource, resource
import wandb.sdk.launch
import wandb.sdk.launch.agent as launch_agent

import wandb.sdk.internal.internal_api as wandb_internal


from .configs import (
       wandb_launch_config,
       wandb_launch_agent_queue_config,
       wandb_launch_agent_config,
       wandb_compute_kubernetes_config,
       wandb_launch_shared_config
)


@resource(
    {"api_key": Field(StringSource, description="Weights & Biases API key")},
    description="Resource for interacting with the wandb SDK",
)
def wandb_resource(context: OpExecutionContext):
    wandb.login(key=context.resource_config["api_key"])
    return wandb


@resource(
    config_schema=wandb_launch_shared_config(), description="Launch Config resource for local single run"
)
def wandb_local_resource(context):
    return wandb.sdk.launch.run(**context.resource_config)


@resource(
    config_schema=wandb_launch_agent_queue_config(), description="Launch Config resource for local single run"
)
def wandb_agent_queue(context):
    return wandb_internal.create_run_queue(**context.resource_config)


@resource(
    config_schema=wandb_launch_agent_config(), description="Launch Agent resource"
)
def wandb_agent(context):
    return launch_agent.LaunchAgent(**context.resource_config)


@resource(
    config_schema=wandb_compute_kubernetes_config(), description="Launch resource Kubernetes"
)
def wandb_launch_kubernetes_resource(context):
    return context.resource_config