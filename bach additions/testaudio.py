from healthchord import play_health_chord

values = [7, 2.1, 120, 8]
targets = [9, 2.9, 120, 8]

score, frequencies = play_health_chord(values, targets)

print("Health deviation score:", score)
print("Audio frequencies:", frequencies)