# PoemsFromAI

Generate poems using seq2seq model.

## Configuration

* tensorflow 1.14 (cpu or gpu)

## Quick Start

1. Clone this repo.
2. Install dependencies.
3. Set `model.GPU` if you'd like to use `CudnnLSTM`; Else `LSTMBlockFusedCell`.
4. Run `train.py`. `wujue` is better for a test.
5. Run `compose.py`. Choose only the trained model.

## Credits

@jinfagang [tensorflow_poems](https://github.com/jinfagang/tensorflow_poems)

## License

[Apache License](https://github.com/JamzumSum/PoemsFromAI/blob/master/LICENSE.md)
