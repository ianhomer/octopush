# Octopush

Playing with [Octopus energy API](https://developer.octopus.energy/rest/reference).

Set environment variables, e.g. with [direnv](https://direnv.net/).

| Variable              |                                                      |
| --------------------- | ---------------------------------------------------- |
| OCTOPUS_MPAN          | MPAN - Meter Point Administration Number             |
| OCTOPUS_SERIAL_NUMBER | Meter serial number                                  |
| OCTOPUS_API_KEY       | API Key from your profile page in the Octopus portal |

Install

    pip install -e .

And get consumption

```sh
❯ octopush --list-consumption
2024-08-30T23:00:00+01:00    0.114
2024-08-30T23:30:00+01:00    0.085
2024-08-31T00:00:00+01:00    0.046
2024-08-31T00:30:00+01:00    0.045
2024-08-31T01:00:00+01:00    0.096
                             ...
2024-09-01T22:30:00+01:00    0.214
2024-09-01T23:00:00+01:00    0.073
2024-09-01T23:30:00+01:00    0.076
2024-09-02T00:00:00+01:00    0.098
2024-09-02T00:30:00+01:00    0.060
Length: 100, dtype: float64
```
