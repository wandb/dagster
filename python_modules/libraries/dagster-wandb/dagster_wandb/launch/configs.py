from dagster import Bool, Field, String, Noneable
from dagster.core.types.dagster_type import Array, Optional
from dagster_wandb.launch.util import utils
import json

def wandb_init_config():
    api_key = Field(
        String,
        description="API Key"
    )
    return {"api_key":  api_key}


def wandb_launch_shared_config():
    uri = Field(
        config=str,
        is_required=False,
        description="URI of experiment to run. A wandb run uri or a Git repository URI",
    )
    entry_point = Field(
        config=Array(str),
        is_required=False,
        description="Entry point of the run. default: main"
    )
    entity = Field(
        config=str,
        is_required=False,
        description="Name of the target entity which the new run will be sent to",
    )
    project = Field(
        config=str,
        is_required=False,
        description="The target project for the launched run"
    )

    return {
        "uri": uri,
        "entry_point": entry_point,
        "entity": entity,
        "project": project
    }


def wandb_launch_add_config():
    shared_conf = wandb_launch_shared_config()

    queue = Field(
        config=Array(str),
        is_required=False,
        description="Run queue to push to",
    )
    return {
            "uri": shared_conf.get("uri"),
            "entry_point": shared_conf.get("entry_point", None),
            "entity": shared_conf["entity"],
            "project": shared_conf["project"],
            "queue" : queue
    }


def wandb_launch_config():
    shared_conf = wandb_launch_shared_config

    queue = Field(
        config=Array(str),
        description="Run queue to push to",
    )

    entity = Field(
        config=str,
        description="The target entity for the launched run",
    )

    project = Field(
        config=str,
        description="The target project for the launched run"
    )

    name = Field(
        config=str,
        description="The run name for the launched run, displayed in th W&B UI"
    )

    git = Field(
        config=str,
        description="The repo URL to use instead of the repo associated with the run"
    )

    docker_image = Field(
        config=str,
        description="the docker image to use"
    )

    cuda = Field(
        config=Bool,
        description="When set to True or when reproducing a previous GPU run, builds a CUDA-enabled image."
    )
    parameters = Field(
        Noneable(float),
        default_value=None,
        description="Parameters (dictionary) for the entry point command. Defaults to using "
                    "the parameters used to run the original run",
    )

    return {
        "launch_job_config": {
            "uri": uri,
            "entity": entity,
            "project":project,
            "name":name,
            "git":git,
            "docker_image":docker_image,
            "cuda":cuda,
            "parameters":parameters
        }
    }

#:TODO
def wandb_launch_agent_queue_config():
    entity = Field(
        String,
        description="The target entity for the launched run"
    )

    project = Field(
        String,
        description="The target project for the launched run"
    )
    name = Field(
        String,
        description="The target entity for the launched run",
    )
    access = Field(
        String,
        default_value="PROJECT",
        description="The target project for the launched run"
    )

    return {
            "entity":entity,
            "project":project,
            "name":name,
            "access":access
    }


def wandb_launch_agent_config():
    entity = Field(
        String,
        is_required=False,
        description="The target entity for the launched run. Defaults to current logged-in user"
    )
    project = Field(
        String,
        is_required=True,
        description="The target project for the launched run"
    )
    queues = Field(
        [String],
        default_value=["default"],
        description="The queue names to poll"
    )
    max_jobs = Field(
        int,
        is_required=False,
        description="The maximum number of launch jobs this agent can run in parallel. Defaults to 1.",
    )
    return {
            "entity": entity,
            "queues": queues,
            "project" : project,
            "max_jobs": max_jobs
    }

# :TODO
def wandb_compute_kubernetes_config():
    sc = wandb_launch_shared_config()
    config_file = Field(
        String,
        description=""
    )

    job_spec = Field(
        String,
        description=""
    )

    registry = Field(
        String,
        description=""
    )

    namespace = Field(
        String,
        description=""
    )
    resource = Field (
        String,
        default_value="kubernetes",
        description=""
    )

    job_name = Field (
        String,
        description=""
    )

    job_labels = Field(
        String,
        description=""
    )
    backoff_limit = Field(
        String,
        description=""
    )


    resource_limits =Field(
        String,
        description=""
    )

    return {
        "uri": sc["uri"],
        "entity": sc["entity"],
        "project": sc["project"],
        "resource":resource,
        "config_file" : config_file,
        "job_spec" : job_spec,
        "registry":registry,
        "namespace" : namespace,
        "resource_limits": resource_limits
    }


def wandb_compute_gcp_config():
    # uri, entity, project
    sc = wandb_launch_shared_config()

    resource = Field(
        String,
        default_value="gcp_vertex",
        description=""
    )
    bucket = Field(
        String,
        default_value="test-bucket",
        description=""
    )

    repo = Field(
        String,
        default_value="test_repo",
        description=""
    )
    return {
        "uri": sc["uri"],
        "entity": sc["entity"],
        "project": sc["project"],
        "resource": resource,
        "staging_bucket": bucket,
        "artifact_repo": repo,
    }


def wandb_compute_aws_config():
    path = "launch_sagemaker_config.json"
    f_path = utils.config_path(path, "../../../")
    kwargs = json.loads(utils.config_open(f_path, "r").read())

    # uri, entity, project
    sc = wandb_launch_shared_config()

    kwargs["uri"] = sc["uri"]
    kwargs["entity"] = sc["entity"]
    kwargs["project"] = sc["project"]
    return kwargs




