from dagster import op
from wandb.sdk.launch import launch as wandb_launch
from wandb.sdk.launch.agent import LaunchAgent as launch_agent
from wandb.errors import LaunchError


from .configs import (
    wandb_launch_agent_config,
    wandb_compute_aws_config,
    wandb_compute_gcp_config,
    wandb_launch_shared_config
)

SUCCEEDED = "Launch.STATE_SUCCEEDED"
FAILED = "Launch.STATE_FAILED"

_DEFAULT_OP_PROPS = dict(
    required_resource_keys={"wandbapi"},
)


@op(
    **_DEFAULT_OP_PROPS,
    config_schema=wandb_launch_shared_config(),
)
def wandb_launch_single_run_op(context):
    """
    wandb Launch Local - single run
    This op encapsulates a launch of single run
    Expects a single run resource to be provisioned and initiate a run.
    Args:
        context:

    Returns:
        submitted_run output

    """
    # print("In wandb_launch_single_run_op")
    context.log.info("executing single_run_op %s" % (context.op_config.get("uri")))

    (uri, entry_point, entity, project) = [context.op_config.get(k) for k in ("uri", "entry_point", "entity", "project")]
    wandb_output = wandb_launch.run(api=context.resources.wandbapi
                                    , uri=uri, entry_point=entry_point
                                    , entity=entity, project=project)
    # print(wandb_output)
    return wandb_output


@op(
    **_DEFAULT_OP_PROPS,
    config_schema=wandb_launch_agent_config()
)
def wandb_launch_agent_op(context):
    """
    WandB launch an agent
    This op encapsulates a launch of an agent.
    Args:
        context:
    Returns:
        a run
    """
    (entity, project, queues, max_jobs) = [context.op_config.get(k) for k in ("entity", "project", "queues", "max_jobs")]

    config = {
        "entity": entity,
        "project": project,
        "queues": queues,
        "max_jobs": max_jobs
    }
    agent = launch_agent(api=context.resources.wandbapi, config=config)
    print(agent.print_status())
    return agent.print_status()


@op(
    **_DEFAULT_OP_PROPS,
    config_schema=wandb_compute_gcp_config()
)
def wandb_launch_gcp_op(context):
    """
    WandB launch single run
    This op encapsulates a launch of a run on kubernetes compute
    Expects a Kubernetes resource config to initiate a run.
    Args:
        context:
    Returns:
        submitted_run output
    """
    (uri, entity, project, resource, staging_bucket, repo) = [context.op_config.get(k) for k in
                                           ("uri", "entity","project", "resource", "staging_bucket", "artifact_repo")]

    kwargs = {
        "uri": uri,
        "api": context.resources.wandbapi,
        "resource": resource,
        "entity": entity,
        "project": project,
        "resource_args": {
            "gcp_vertex": {
                "staging_bucket": staging_bucket,
                "artifact_repo": repo,
            },
        },
    }

    try:
        run = wandb_launch.run(**kwargs)
        run_id = run.id
        run_state = SUCCEEDED
        run_name = run.name
        gcp_project = run.gcp_project
        error = None


    except LaunchError as e:
        run_id = None
        run_state = FAILED
        run_name = None
        gcp_project = None
        error = e.message
        # print(e.message)

    return {
        "run.id": run_id,
        "run_state": run_state,
        "run_name": run_name,
        "run.gcp_project": gcp_project,
        "error": error
    }


@op(
    **_DEFAULT_OP_PROPS,
    config_schema=wandb_compute_aws_config()
)
def wandb_launch_aws_op(context):
    """
    WandB launch single run
    This op encapsulates a launch of a run on kubernetes compute
    Expects a Kubernetes resource config to initiate a run.
    Args:
        context:
    Returns:
        submitted_run output
    """
    kwargs = context.op_config
    try:
        run = wandb_launch.run(**kwargs)
        run_id = run.id
        run_state = SUCCEEDED
        run_name = run.get_status()
        error = None


    except LaunchError as e:
        run_id = None
        run_state = FAILED
        run_name = None
        error = e.message
        print(e.message)

    return {
        "run.id": run_id,
        "run_state": run_state,
        "run_name": run_name,
        "error": error
    }

