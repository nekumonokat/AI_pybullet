# AI_pybullet
This project focuses on recreating Karl Sims project of creature generation. It consists codes that aid in genetic encoding, creating creatures with motors using the DNA and a fitness function to determine the fittest creature to display its movements.

A threaded simulation was added, but it doesn't work on windows, as such a modified method was done. An offline simulation was also added.

When testing the best gene count, it was noticed that the best would be the highest, but due to computational power, the max chosen would be 8. [genecount_analysis.py]

Things to be modified:
- link length [scale 1]: 0.1, 0.5 and 0.9 will be chosen
- link radius [scale 1]: 0.1, 0.5 and 0.9 will be chosen
- link mass [scale 1]: 0.3, 0.5, 0.7 and 0.9 will be chosen
- joint type: [0.1 FIXED], [0.9 REVOLUTE]
- control waveform : [0.1 PULSE], [0.9 SINE]
- control amp [scale 0.25]
- control freq [scale 1]