import pytest

from dagster_wandb.launch.ops import (
    wandb_launch_single_run_op,
    wandb_launch_gcp_op,
    wandb_launch_add_op,
    # wandb_launch_aws_op,
    wandb_launch_agent_op
)
from dagster_wandb.resources import wandb_api_resource
from dagster import job
from dagster_wandb.launch.util import utils
import json


def test_wandb_launch_local_op():
    @job(resource_defs={"wandbapi":wandb_api_resource})
    def launch_single_run():
        wandb_launch_single_run_op.alias("single_run_op")()
    result = launch_single_run.execute_in_process(
            run_config={"ops": {"single_run_op": {"config": {"uri": "https://wandb.ai/ash-shaik/dagster_wandb_run/runs/3adqksme"
                                                         # , "entry_point": ["python", "train.py"]
                                                          , "entity": "ash-shaik"
                                                          , "project" : "dagster-launch"
                                                          }}}
                        ,'resources': {'wandbapi': {'config': {'api_key': 'test-key'}}}
                        }
        )
    assert result.success
    #wandb_launch_op_()


def test_wandb_launch_add_op():
    @job(resource_defs={"wandbapi":wandb_api_resource})
    def launch_add():
        wandb_launch_add_op.alias("launch_add_op")()
    result = launch_add.execute_in_process(
            run_config={"ops": {"launch_add_op": {"config": {"uri": "https://wandb.ai/ash-shaik/dagster-launch/runs/2ra0v32q"
                                                         # , "entry_point": ["python", "train.py"]
                                                          , "entity": "ash-shaik"
                                                          , "project" : "dagster-launch"
                                                          , "queue" : ['default']
                                                          }}}
                        ,'resources': {'wandbapi': {'config': {'api_key': 'test-key'}}}
                        }
        )
    assert result.success
    #wandb_launch_op_()


def test_wandb_launch_agent_op():
    @job(resource_defs={"wandbapi": wandb_api_resource})
    def launch_local_agent():
        wandb_launch_agent_op.alias("launch_local_agent_op")()

    result = launch_local_agent.execute_in_process(
        run_config={ "ops": {"launch_local_agent_op" : {"config":{
             "entity": "wandb-data-science"
            , "project" : "dagster-launch"
            , "max_jobs" : 2
        }}}

            , 'resources': {'wandbapi': {'config': {'api_key': 'test-key'}}}

        })
    assert result.success


def test_wandb_launch_gcp_op():
    @job(resource_defs={"wandbapi":wandb_api_resource})
    def launch_gcp_run():
        wandb_launch_gcp_op.alias("gcp_run_op")()
    result = launch_gcp_run.execute_in_process(
            run_config={"ops": {"gcp_run_op": {"config": {"uri": "https://wandb.ai/mock_server_entity/test/runs/1"
                                                          , "entity": "mock_server_entity"
                                                          , "project" : "test"
                                                          , "staging_bucket": "test-bucket"
                                                          , "artifact_repo": "test_repo",
                                                          }}}
                        ,'resources': {'wandbapi': {'config': {'api_key': 'test'}}}
                        }
        )
    print(result._output_capture.get("error"))
    assert result.success


@pytest.mark.skip
def test_wandb_launch_aws_op():
    @job(resource_defs={"wandbapi":wandb_api_resource})
    def launch_aws_run():
        path = "launch_sagemaker_config.json"

        f_path = utils.config_path(path, "../")
        kwargs = json.loads(utils.config_open(f_path, "r").read())
        kwargs["uri"] = "https://wandb.ai/mock_server_entity/test/runs/1"
        kwargs["entity"] = "mock_server_entity"
        kwargs["project"] = "test"


        wandb_launch_aws_op.alias("aws_run_op")()
    result = launch_aws_run.execute_in_process(
            run_config={"ops": {"aws_run_op": {"config": {}}}
                        ,'resources': {'wandbapi': {'config': {'api_key': 'test'}}}
                        }
        )
    print(result._output_capture.get("error"))
    assert result.success



