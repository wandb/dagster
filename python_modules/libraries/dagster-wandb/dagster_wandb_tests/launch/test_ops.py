from dagster_wandb.launch.ops import wandb_launch_single_run_op
from dagster import job

'''
my_wandb_resource = wandb_launch_config.configured(
        {"api_key": {"env": "WANDB_API"}})
'''

# wandb_launch_op_ = wandb_launch_single_run_op.configured({"uri": "https://wandb.ai/wandb/launch-welcome/runs/2er1eom2"}
#                                                        , name="local single run")

wandb_launch_op_ = wandb_launch_single_run_op.configured({"uri": "https://wandb.ai/wandb/launch-welcome/runs/2er1eom2"
                                                          , "entry_point": "python train.py"
                                                          , "entity": "wandb-data-science"
                                                          , "project" : "launch_testing"
                                                          }, name = "single_run_launch")



def test_wandb_launch_op():
    @job
    def launch_single_run():
        wandb_launch_single_run_op.alias("single_run_op")()
    result = launch_single_run.execute_in_process(
            run_config={"ops": {"single_run_op": {"config": {"uri": "https://github.com/stephchen/sc-pytorch-mnist"
                                                          , "entry_point": "python train.py"
                                                          , "entity": "wandb-data-science"
                                                          , "project" : "launch_testing"
                                                          }}}}
        )
    assert result.success
    #wandb_launch_op_()







