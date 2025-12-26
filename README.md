# twistedpair
A system model along with simulation environment for high-speed SerDes.

Tx ---> Channel ---> Rx

Waveformes are simulated at multiple of the nyquist rate.
Simulation is done on blocks of samples. Dynamic loop behaviour is modeled by going through a block of samples, batch by batch.
Not suitable for live-streaming but can create animations to mimic live streaming.

Analysis tools include eye diagram, spectral monitoring, bathtub curves and more.
