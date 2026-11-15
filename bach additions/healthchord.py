
import numpy as np
import sounddevice as sd


def play_health_chord(values, targets, duration=3.0, sample_rate=44100, volume=0.3):

    values = np.array(values, dtype=float)
    targets = np.array(targets, dtype=float)

    if len(values) != len(targets) or len(values) == 0:
        raise ValueError("Values and targets must have the same non-zero length.")

    if np.any(targets == 0):
        raise ValueError("Target values must be non-zero for percentage deviation.")

    # Health deviation
    deviations = np.abs(values - targets) / np.abs(targets)

    score = np.mean(deviations)
    score = np.clip(score, 0, 1)

    # C4, E4, G4
    base_notes = np.array([60, 64, 67], dtype=float)

    # Increase dissonance as the score increases
    # Maximum: C4, Bb4, C#4
    shifts = np.array([0, 6, -6]) * score

    midi_notes = base_notes + shifts

    frequencies = 440 * (2 ** ((midi_notes - 69) / 12))

    #Audio
    t = np.linspace(
        0, duration,
        int(sample_rate * duration),
        endpoint=False
    )

    audio = np.zeros(len(t))

    for frequency in frequencies:
        audio += np.sin(2 * np.pi * frequency * t)

    audio = audio / 3 * volume

    # Smoother fade
    fade_length = int(sample_rate * 0.05)

    envelope = np.ones(len(audio))
    envelope[:fade_length] = np.linspace(0, 1, fade_length)
    envelope[-fade_length:] = np.linspace(1, 0, fade_length)

    audio *= envelope

    sd.play(audio, sample_rate)
    sd.wait()

    return score, frequencies
