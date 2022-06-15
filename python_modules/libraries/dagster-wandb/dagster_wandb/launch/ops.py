from dagster import In, Nothing, Out, op
from wandb.sdk.launch import launch as wandb_launch

from .configs import (
    wandb_launch_config,
    wandb_launch_agent_config,
    wandb_compute_kubernetes_config,
    wandb_compute_gcp_config,
    wandb_launch_shared_config
)

_DEFAULT_OP_PROPS = dict(
    required_resource_keys={"wandb"},
    ins={"start_after": In(Nothing)},
    out=Out(str, description="output from running the wandb command."),
    tags={"kind": "wandb"},
)


@op(
    # **_DEFAULT_OP_PROPS,
    config_schema=wandb_launch_shared_config()
)
def wandb_launch_single_run_op(context):
    """
    WandB launch single run
    This op encapsulates a launch of single run

    Expects a single run resource to be provisioned and initiate a run.

    Args:
        context:

    Returns:
        submitted_run output

    """
    print("In wandb_launch_single_run_op")
    context.log.info("executing single_run_op %s" % (context.op_config.get("uri")))
    wandb_output = wandb_launch.run(**context.op_config)
    # wandb_output = context.resources.launch.wandb_local_resource(**context.resource_config)
    print(wandb_output)
    return wandb_output


@op(
    config_schema=wandb_launch_agent_config()
)
def wandb_launch_agent(context):
    """
    WandB launch an agent
    This op encapsulates a launch of an agent.
    Args:
        context:
    Returns:
        a run
    """
    return context.resources.launch(**context.resource_config)


@op(
    config_schema=wandb_compute_kubernetes_config()
)
def wandb_launch_kubernetes(context):
    """
    WandB launch single run
    This op encapsulates a launch of a run on kubernetes compute
    Expects a Kubernetes resource config to initiate a run.
    Args:
        context:
    Returns:
        submitted_run output
    """
    return wandb.sdk.launch.launch(**context.resource_config)


@op(
    config_schema=wandb_compute_gcp_config()
)
def wandb_launch_gcp(context):
    """
    WandB launch single run
    This op encapsulates a launch of run on GCP compute
    Expects a GCP resource config to initiate a run.
    Args:
        context:
    Returns:
        submitted_run output
    """
    return wandb.sdk.launch.launch(**context.resource_config)


