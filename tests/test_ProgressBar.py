from recipys.ProgressBar import ProgressBar


def test_ProgressBar(capsys):
    steps: int = 5

    with ProgressBar(total_steps=steps) as bar:

        for step in range(steps - 1):
            bar.advance()
            assert not bar._progress.finished

        bar.advance()
        assert bar._progress.finished
