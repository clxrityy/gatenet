# gatenet.radio

RF signal detection, classification, and mesh integration.

## Features

- Frequency scanning
- ADS-B decoding
- Weather station decoding
- Event-driven signal callbacks

## Example Usage

```python
from gatenet.radio.base import RadioInterface
radio = RadioInterface()
radio.scan_frequencies(433_000_000, 434_000_000, 10)
radio.on_signal(lambda info: print(info))
```
