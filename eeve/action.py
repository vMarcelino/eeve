class Action:
    def __init__(self, f, run_args, run_kwargs):
        self.func = f
        self.run_args = run_args
        self.run_kwargs = run_kwargs