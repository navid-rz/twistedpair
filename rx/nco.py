class NCO:
    """
    Numerically Controlled Oscillator for CDR clock recovery.
    Maintains phase and frequency, updates phase using loop filter output.
    """
    
    
    def __init__(self, sps, init_phase=0.0, init_freq=1.0, phase_modulo=None):
        self.sps = sps  # samples per symbol
        self.phase = init_phase  # phase accumulator (in samples)
        self.freq = init_freq    # frequency increment per symbol (samples/symbol)
        self.phase_modulo = phase_modulo if phase_modulo is not None else sps

    def update_bang_bang(self, phase_error, nominal_freq=None, kp=0.01):
        """
        Classic bang-bang CDR update: only phase correction per symbol.
        Args:
            phase_error: Phase error from phase detector
            nominal_freq: Nominal frequency increment (samples/symbol, default: self.sps)
            kp: Proportional gain
        Note:
            Bang-bang CDR requires at least 2 samples per symbol (early/late).
        """
        if nominal_freq is None:
            nominal_freq = self.sps
        self.phase += nominal_freq + kp * phase_error
        # Wrap phase accumulator
        if self.phase >= self.phase_modulo:
            self.phase -= self.phase_modulo
        elif self.phase < 0:
            self.phase += self.phase_modulo

    def update_digital_pll(self, phase_error, kp=0.01, ki=0.001):
        """
        Update NCO phase and frequency using PI controller output.
        Args:
            phase_error: Phase error from phase detector
            kp: Proportional gain
            ki: Integral gain
        """
        # Simple PI controller for demonstration
        self.freq += ki * phase_error
        self.phase += self.freq + kp * phase_error
        # Wrap phase accumulator
        if self.phase >= self.phase_modulo:
            self.phase -= self.phase_modulo
        elif self.phase < 0:
            self.phase += self.phase_modulo

    def get_sample_index(self):
        """
        Get current sample index for waveform sampling.
        Returns:
            Integer sample index
        """
        return int(round(self.phase))

    def reset(self, phase=0.0, freq=1.0):
        self.phase = phase
        self.freq = freq
