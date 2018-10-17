from __future__ import division, absolute_import, print_function, unicode_literals
from collections import OrderedDict
from .constants import Register, RF, HW
from .register_value import RegisterValue
from .register_area import RegisterArea


class OpMode(RegisterValue):
    REGISTER = 0x01
    FORMAT = [('disable_sequencer', 1), ('listen', 1), ('listen_abort', 1), ('mode', 3), (0b00, 2)]

    Sleep = 0b000
    Standby = 0b001
    FS = 0b010
    TX = 0b011
    RX = 0b100

    def __init__(self):
        self.disable_sequencer = False
        self.listen = False
        self.listen_abort = False
        self.mode = self.Standby


class DataModulation(RegisterValue):
    REGISTER = 0x02
    FORMAT = [(False, 1), ('data_mode', 2), ('modulation_type', 2), (False, 1), ('modulation_shaping', 2)]

    ModePacket           = 0b00
    ModeContinuousSync   = 0b10
    ModeContinuousNoSync = 0b11

    TypeFSK              = 0b00
    TypeOOK              = 0b01

    def __init__(self):
        self.data_mode = self.ModePacket
        self.modulation_type = self.TypeFSK
        self.modulation_shaping = 0b00

        
class AfcFei(RegisterValue):
    REGISTER = Register.AFCFEI
    FORMAT = [(False, 1), ('fei_done', 1), ('fei_start', 1), ('afc_done', 1),
             ('afc_autoclear_on', 1), ('afc_auto_on', 1), ('afc_clear', 1), ('afc_start', 1)]
             
    def __init__(self):
        self.fei_done = False
        self.fei_start = False
        self.afc_done = True
        self.afc_autoclear_on = False
        self.afc_auto_on = False
        self.afc_clear = False
        self.afc_start = False

class RSSIConfig(RegisterValue):
    REGISTER = 0x23
    FORMAT = [(False, 6), ('rssi_done', 1), ('rssi_start', 1)]

    def __init__(self):
        self.rssi_done = True
        self.rssi_start = False


class IRQFlags1(RegisterValue):
    REGISTER = 0x27
    FORMAT = [('mode_ready', 1), ('rx_ready', 1), ('tx_ready', 1), ('pll_lock', 1), ('rssi', 1),
              ('timeout', 1), ('auto_mode', 1), ('sync_address_match', 1)]

    def __init__(self):
        self.mode_ready = True
        self.rx_ready = False
        self.tx_ready = False
        self.pll_lock = False
        self.rssi = False
        self.timeout = False
        self.auto_mode = False
        self.sync_address_match = False


class IRQFlags2(RegisterValue):
    REGISTER = 0x28
    FORMAT = [('fifo_full', 1), ('fifo_not_empty', 1), ('fifo_level', 1), ('fifo_overrun', 1), ('packet_sent', 1),
              ('payload_ready', 1), ('crc_ok', 1), (False, 1)]

    def __init__(self):
        self.fifo_full = False
        self.fifo_not_empty = False
        self.fifo_level = False
        self.fifo_overrun = False
        self.packet_sent = False
        self.payload_ready = False
        self.crc_ok = False


class PacketConfig1(RegisterValue):
    REGISTER = 0x37
    FORMAT = [('variable_length', 1), ('dc_free', 2), ('crc', 1), ('crc_auto_clear_off', 1), ('address_filtering', 2),
              (False, 1)]

    DCFreeOff           = 0b00
    DCFreeManchester    = 0b01
    DCFreeWhitening     = 0b10

    def __init__(self):
        self.variable_length = False
        self.dc_free = self.DCFreeOff
        self.crc = True
        self.crc_auto_clear_off = False
        self.address_filtering = 0b00


class Temperature1(RegisterValue):
    REGISTER = 0x4E
    FORMAT = [(False, 4), ('start', 1), ('running', 1), (0b01, 2)]

    def __init__(self):
        self.start = False
        self.running = False

        
class DioMapping1(RegisterValue):
    REGISTER = 0x25
    FORMAT = [('dio0', 2), ('dio1', 2), ('dio2', 2), ('dio3', 2)]
	
    DIOMAPPING_00 = 0
    DIOMAPPING_01 = 1
    DIOMAPPING_10 = 2
    DIOMAPPING_11 = 3
	
    def __init__(self):
        self.dio0 = self.DIOMAPPING_00
        self.dio1 = self.DIOMAPPING_00
        self.dio2 = self.DIOMAPPING_00
        self.dio3 = self.DIOMAPPING_00

class DioMapping2(RegisterValue):
    REGISTER = 0x26
    FORMAT = [('dio4', 2), ('dio5', 2), (False, 1), ('clkout', 3)]
    
    DIOMAPPING_00 = 0
    DIOMAPPING_01 = 1
    DIOMAPPING_10 = 2
    DIOMAPPING_11 = 3
    
    CLKOUT_1 = 0
    CLKOUT_2 = 1
    CLKOUT_4 = 2
    CLKOUT_8 = 3
    CLKOUT_16 = 4
    CLKOUT_32 = 5
    CLKOUT_RC = 6
    CLKOUT_OFF = 7
    
    def __init__(self):
        self.dio4 = self.DIOMAPPING_00
        self.dio5 = self.DIOMAPPING_00
        self.clkout = self.CLKOUT_OFF
        
        
class Frequency(RegisterArea):
    BASEREGISTER = Register.FRFMSB
    VALUES = []
    
    def __init__(self):
        self.VALUES.append(RF.FRFMSB_915)
        self.VALUES.append(RF.FRFMID_915)
        self.VALUES.append(RF.FRFLSB_915)
        
    def set_mhz(self, MHz):
        fword = int(round(MHz * 1E6 / HW.FSTEP))
        self.set_word(fword)

        
class Bitrate(RegisterArea):
    BASEREGISTER = Register.BITRATEMSB
    VALUES = []
    
    def __init__(self):
        self.VALUES.append(RF.BITRATEMSB_4800)
        self.VALUES.append(RF.BITRATELSB_4800)
        
    def set_bps(self, bps):
        rateword = int(round(HW.FXOSC / bps))
        self.set_word(rateword)
        

class Deviation(RegisterArea):
    BASEREGISTER = Register.FDEVMSB
    VALUES = []
    
    def __init__(self):
        self.VALUES.append(RF.FDEVMSB_5000)
        self.VALUES.append(RF.FDEVLSB_5000)
        
    def set_khz(self, khz):
        devword = int(round(khz * 1000 / HW.FSTEP))
        self.set_word(devword)

class RFM69Configuration(object):
    """ An object to hold to represent the configuration of the RFM69. There's quite a bit of it.

        Some of the most-used registers are RegisterValue objects which remove the need for bitwise arithmetic.
    """
    def __init__(self):
        """ Defaults here are *mostly* the same as the defaults on the RFM69W """
        self.opmode = OpMode()
        self.data_modulation = DataModulation()

        self.bitrate = Bitrate()
        self.fdev = Deviation()
        self.frf = Frequency()

        self.afc_ctl = RF.AFCLOWBETA_OFF

        self.pa_level = RF.PALEVEL_PA0_ON | RF.PALEVEL_PA1_OFF | RF.PALEVEL_PA2_OFF | 0x18
        self.pa_ramp = RF.PARAMP_40

        self.ocp = RF.OCP_ON | RF.OCP_TRIM_95
        self.lna = RF.LNA_ZIN_200
        self.rx_bw = RF.RXBW_DCCFREQ_010 | RF.RXBW_MANT_24 | RF.RXBW_EXP_5
        self.rx_afc_bw = RF.RXBW_DCCFREQ_010 | RF.RXBW_MANT_24 | RF.RXBW_EXP_5
        self.afc_fei = AfcFei()

        self.dio_mapping_1 = DioMapping1()
        self.dio_mapping_2 = DioMapping2()

        self.rssi_threshold = 200

        self.rx_timeout_1 = 0
        self.rx_timeout_2 = 40

        self.sync_config = RF.SYNC_ON | RF.SYNC_FIFOFILL_AUTO | RF.SYNC_SIZE_4 | RF.SYNC_TOL_0
        self.sync_value_1 = 0
        self.sync_value_2 = 0
        self.sync_value_3 = 0
        self.sync_value_4 = 0
        self.sync_value_5 = 0
        self.sync_value_6 = 0
        self.sync_value_7 = 0
        self.sync_value_8 = 0

        self.packet_config_1 = PacketConfig1()
        self.payload_length = 0x40

        self.fifo_threshold = RF.FIFOTHRESH_TXSTART_FIFONOTEMPTY | RF.FIFOTHRESH_VALUE
        self.packet_config_2 = RF.PACKET2_RXRESTARTDELAY_2BITS | RF.PACKET2_AUTORXRESTART_ON | RF.PACKET2_AES_OFF
        self.test_dagc = RF.DAGC_IMPROVED_LOWBETA0
        self.test_afc = 0x0e

    def get_registers(self):
        regs = OrderedDict()
        regs[Register.OPMODE] = self.opmode.pack()
        regs[Register.DATAMODUL] = self.data_modulation.pack()

        for register, value in self.bitrate.pack().iteritems():
            regs[register] = value
        
        for register, value in self.fdev.pack().iteritems():
            regs[register] = value
            
        for register, value in self.frf.pack().iteritems():
            regs[register] = value
            
        regs[Register.AFCCTRL] = self.afc_ctl
        regs[Register.PALEVEL] = self.pa_level
        regs[Register.PARAMP] = self.pa_ramp
        regs[Register.OCP] = self.ocp
        regs[Register.LNA] = self.lna
        regs[Register.RXBW] = self.rx_bw
        regs[Register.AFCBW] = self.rx_afc_bw
        regs[Register.AFCFEI] = self.afc_fei.pack()
        regs[Register.DIOMAPPING1] = self.dio_mapping_1.pack()
        regs[Register.DIOMAPPING2] = self.dio_mapping_2.pack()
        regs[Register.RSSITHRESH] = self.rssi_threshold
        regs[Register.RXTIMEOUT1] = self.rx_timeout_1
        regs[Register.RXTIMEOUT2] = self.rx_timeout_2
        regs[Register.SYNCCONFIG] = self.sync_config
        regs[Register.SYNCVALUE1] = self.sync_value_1
        regs[Register.SYNCVALUE2] = self.sync_value_2
        regs[Register.SYNCVALUE3] = self.sync_value_3
        regs[Register.SYNCVALUE4] = self.sync_value_4
        regs[Register.SYNCVALUE5] = self.sync_value_5
        regs[Register.SYNCVALUE6] = self.sync_value_6
        regs[Register.SYNCVALUE7] = self.sync_value_7
        regs[Register.SYNCVALUE8] = self.sync_value_8
        regs[Register.PACKETCONFIG1] = self.packet_config_1.pack()
        regs[Register.PAYLOADLENGTH] = self.payload_length
        regs[Register.FIFOTHRESH] = self.fifo_threshold
        regs[Register.PACKETCONFIG2] = self.packet_config_2
        regs[Register.TESTDAGC] = self.test_dagc
        regs[Register.TESTAFC]  = self.test_afc
        regs[255] = 0
        return regs
