class emeterPacket:
    SMA_POSITIVE_ACTIVE_POWER = 0x00010400
    SMA_POSITIVE_ACTIVE_POWER_L1 = 0x00150400
    SMA_POSITIVE_ACTIVE_POWER_L2 = 0x00290400
    SMA_POSITIVE_ACTIVE_POWER_L3 = 0x003D0400
    SMA_POSITIVE_ACTIVE_ENERGY = 0x00010800
    SMA_POSITIVE_ACTIVE_ENERGY_L1 = 0x00150800
    SMA_POSITIVE_ACTIVE_ENERGY_L2 = 0x00290800
    SMA_POSITIVE_ACTIVE_ENERGY_L3 = 0x003D0800
    SMA_NEGATIVE_ACTIVE_POWER = 0x00020400
    SMA_NEGATIVE_ACTIVE_POWER_L1 = 0x00160400
    SMA_NEGATIVE_ACTIVE_POWER_L2 = 0x002A0400
    SMA_NEGATIVE_ACTIVE_POWER_L3 = 0x003E0400
    SMA_NEGATIVE_ACTIVE_ENERGY = 0x00020800
    SMA_NEGATIVE_ACTIVE_ENERGY_L1 = 0x00160800
    SMA_NEGATIVE_ACTIVE_ENERGY_L2 = 0x002A0800
    SMA_NEGATIVE_ACTIVE_ENERGY_L3 = 0x003E0800
    SMA_POSITIVE_REACTIVE_POWER = 0x00030400
    SMA_POSITIVE_REACTIVE_POWER_L1 = 0x00170400
    SMA_POSITIVE_REACTIVE_POWER_L2 = 0x002B0400
    SMA_POSITIVE_REACTIVE_POWER_L3 = 0x003F0400
    SMA_POSITIVE_REACTIVE_ENERGY = 0x00030800
    SMA_POSITIVE_REACTIVE_ENERGY_L1 = 0x00170800
    SMA_POSITIVE_REACTIVE_ENERGY_L2 = 0x002B0800
    SMA_POSITIVE_REACTIVE_ENERGY_L3 = 0x003F0800
    SMA_NEGATIVE_REACTIVE_POWER = 0x00040400
    SMA_NEGATIVE_REACTIVE_POWER_L1 = 0x00180400
    SMA_NEGATIVE_REACTIVE_POWER_L2 = 0x002C0400
    SMA_NEGATIVE_REACTIVE_POWER_L3 = 0x00400400
    SMA_NEGATIVE_REACTIVE_ENERGY = 0x00040800
    SMA_NEGATIVE_REACTIVE_ENERGY_L1 = 0x00180800
    SMA_NEGATIVE_REACTIVE_ENERGY_L2 = 0x002C0800
    SMA_NEGATIVE_REACTIVE_ENERGY_L3 = 0x00400800
    SMA_POSITIVE_APPARENT_POWER = 0x00090400
    SMA_POSITIVE_APPARENT_POWER_L1 = 0x001D0400
    SMA_POSITIVE_APPARENT_POWER_L2 = 0x00310400
    SMA_POSITIVE_APPARENT_POWER_L3 = 0x00450400
    SMA_POSITIVE_APPARENT_ENERGY = 0x00090800
    SMA_POSITIVE_APPARENT_ENERGY_L1 = 0x001D0800
    SMA_POSITIVE_APPARENT_ENERGY_L2 = 0x00310800
    SMA_POSITIVE_APPARENT_ENERGY_L3 = 0x00450800
    SMA_NEGATIVE_APPARENT_POWER = 0x000A0400
    SMA_NEGATIVE_APPARENT_POWER_L1 = 0x001E0400
    SMA_NEGATIVE_APPARENT_POWER_L2 = 0x00320400
    SMA_NEGATIVE_APPARENT_POWER_L3 = 0x00460400
    SMA_NEGATIVE_APPARENT_ENERGY = 0x000A0800
    SMA_NEGATIVE_APPARENT_ENERGY_L1 = 0x001E0800
    SMA_NEGATIVE_APPARENT_ENERGY_L2 = 0x00320800
    SMA_NEGATIVE_APPARENT_ENERGY_L3 = 0x00460800
    SMA_POWER_FACTOR = 0x000D0400
    SMA_POWER_FACTOR_L1 = 0x00210400
    SMA_POWER_FACTOR_L2 = 0x00350400
    SMA_POWER_FACTOR_L3 = 0x00490400
    SMA_CURRENT_L1 = 0x001F0400
    SMA_CURRENT_L2 = 0x00330400
    SMA_CURRENT_L3 = 0x00470400
    SMA_VOLTAGE_L1 = 0x00020400
    SMA_VOLTAGE_L2 = 0x00340400
    SMA_VOLTAGE_L3 = 0x00480400
    SMA_VERSION = 0x90000000

    INITIAL_PAYLOAD_LENGTH = 12
    METER_PACKET_SIZE = 1000

    def __init__(self, serNo=0):
        self.meterPacket = bytearray(self.METER_PACKET_SIZE)
        self.initEmeterPacket(serNo)
        self.begin(0)
        self.end()

    def init(self, serNo):
        self.initEmeterPacket(serNo)

    def begin(self, timeStampMs):
        self._pPacketPos = self._headerLength
        self.storeU32BE(self._pMeterTime, timeStampMs)
        self._length = self.INITIAL_PAYLOAD_LENGTH
        
        # Add dummy values for measurements to make sure the package always contains these. Solves tripower inverters not recognizing the data as valid.
        # Totals
        self.addMeasurementValue(emeterPacket.SMA_POSITIVE_ACTIVE_POWER, 0)
        self.addCounterValue(emeterPacket.SMA_POSITIVE_ACTIVE_ENERGY, 0)
        self.addMeasurementValue(emeterPacket.SMA_NEGATIVE_ACTIVE_POWER, 0)
        self.addCounterValue(emeterPacket.SMA_NEGATIVE_ACTIVE_ENERGY, 0)
        self.addMeasurementValue(emeterPacket.SMA_POSITIVE_REACTIVE_POWER, 0)
        self.addCounterValue(emeterPacket.SMA_POSITIVE_REACTIVE_ENERGY, 0)
        self.addMeasurementValue(emeterPacket.SMA_NEGATIVE_REACTIVE_POWER, 0)
        self.addCounterValue(emeterPacket.SMA_NEGATIVE_REACTIVE_ENERGY, 0)
        self.addMeasurementValue(emeterPacket.SMA_POSITIVE_APPARENT_POWER, 0)
        self.addCounterValue(emeterPacket.SMA_POSITIVE_APPARENT_ENERGY, 0)
        self.addMeasurementValue(emeterPacket.SMA_NEGATIVE_APPARENT_POWER, 0)
        self.addCounterValue(emeterPacket.SMA_NEGATIVE_APPARENT_ENERGY, 0)
        self.addMeasurementValue(emeterPacket.SMA_POWER_FACTOR, 0)

        #L1
        self.addMeasurementValue(emeterPacket.SMA_POSITIVE_ACTIVE_POWER_L1, 0)
        self.addCounterValue(emeterPacket.SMA_POSITIVE_ACTIVE_ENERGY_L1, 0)
        self.addMeasurementValue(emeterPacket.SMA_NEGATIVE_ACTIVE_POWER_L1, 0)
        self.addCounterValue(emeterPacket.SMA_NEGATIVE_ACTIVE_ENERGY_L1, 0)
        self.addMeasurementValue(emeterPacket.SMA_POSITIVE_REACTIVE_POWER_L1, 0)
        self.addCounterValue(emeterPacket.SMA_POSITIVE_REACTIVE_ENERGY_L1, 0)
        self.addMeasurementValue(emeterPacket.SMA_NEGATIVE_REACTIVE_POWER_L1, 0)
        self.addCounterValue(emeterPacket.SMA_NEGATIVE_REACTIVE_ENERGY_L1, 0)
        self.addMeasurementValue(emeterPacket.SMA_POSITIVE_APPARENT_POWER_L1, 0)
        self.addCounterValue(emeterPacket.SMA_POSITIVE_APPARENT_ENERGY_L1, 0)
        self.addMeasurementValue(emeterPacket.SMA_NEGATIVE_APPARENT_POWER_L1, 0)
        self.addCounterValue(emeterPacket.SMA_NEGATIVE_APPARENT_ENERGY_L1, 0)
        self.addMeasurementValue(emeterPacket.SMA_CURRENT_L1, 0)
        self.addMeasurementValue(emeterPacket.SMA_VOLTAGE_L1, 0)
        self.addMeasurementValue(emeterPacket.SMA_POWER_FACTOR_L1, 0) 

        #L2
        self.addMeasurementValue(emeterPacket.SMA_POSITIVE_ACTIVE_POWER_L2, 0)
        self.addCounterValue(emeterPacket.SMA_POSITIVE_ACTIVE_ENERGY_L2, 0)
        self.addMeasurementValue(emeterPacket.SMA_NEGATIVE_ACTIVE_POWER_L2, 0)
        self.addCounterValue(emeterPacket.SMA_NEGATIVE_ACTIVE_ENERGY_L2, 0)
        self.addMeasurementValue(emeterPacket.SMA_POSITIVE_REACTIVE_POWER_L2, 0)
        self.addCounterValue(emeterPacket.SMA_POSITIVE_REACTIVE_ENERGY_L2, 0)
        self.addMeasurementValue(emeterPacket.SMA_NEGATIVE_REACTIVE_POWER_L2, 0)
        self.addCounterValue(emeterPacket.SMA_NEGATIVE_REACTIVE_ENERGY_L2, 0)
        self.addMeasurementValue(emeterPacket.SMA_POSITIVE_APPARENT_POWER_L2, 0)
        self.addCounterValue(emeterPacket.SMA_POSITIVE_APPARENT_ENERGY_L2, 0)
        self.addMeasurementValue(emeterPacket.SMA_NEGATIVE_APPARENT_POWER_L2, 0)
        self.addCounterValue(emeterPacket.SMA_NEGATIVE_APPARENT_ENERGY_L2, 0)
        self.addMeasurementValue(emeterPacket.SMA_CURRENT_L2, 0)
        self.addMeasurementValue(emeterPacket.SMA_VOLTAGE_L2, 0)
        self.addMeasurementValue(emeterPacket.SMA_POWER_FACTOR_L2, 0)

        #L3
        self.addMeasurementValue(emeterPacket.SMA_POSITIVE_ACTIVE_POWER_L3, 0)
        self.addCounterValue(emeterPacket.SMA_POSITIVE_ACTIVE_ENERGY_L3, 0)
        self.addMeasurementValue(emeterPacket.SMA_NEGATIVE_ACTIVE_POWER_L3, 0)
        self.addCounterValue(emeterPacket.SMA_NEGATIVE_ACTIVE_ENERGY_L3, 0)
        self.addMeasurementValue(emeterPacket.SMA_POSITIVE_REACTIVE_POWER_L3, 0)
        self.addCounterValue(emeterPacket.SMA_POSITIVE_REACTIVE_ENERGY_L3, 0)
        self.addMeasurementValue(emeterPacket.SMA_NEGATIVE_REACTIVE_POWER_L3, 0)
        self.addCounterValue(emeterPacket.SMA_NEGATIVE_REACTIVE_ENERGY_L3, 0)
        self.addMeasurementValue(emeterPacket.SMA_POSITIVE_APPARENT_POWER_L3, 0)
        self.addCounterValue(emeterPacket.SMA_POSITIVE_APPARENT_ENERGY_L3, 0)
        self.addMeasurementValue(emeterPacket.SMA_NEGATIVE_APPARENT_POWER_L3, 0)
        self.addCounterValue(emeterPacket.SMA_NEGATIVE_APPARENT_ENERGY_L3, 0)
        self.addMeasurementValue(emeterPacket.SMA_CURRENT_L3, 0)
        self.addMeasurementValue(emeterPacket.SMA_VOLTAGE_L3, 0)
        self.addMeasurementValue(emeterPacket.SMA_POWER_FACTOR_L3, 0)

    def addMeasurementValue(self, id, value):
        self._pPacketPos = self.storeU32BE(self._pPacketPos, id)
        self._pPacketPos = self.storeU32BE(self._pPacketPos, value)
        self._length += 8

    def addCounterValue(self, id, value):
        self._pPacketPos = self.storeU32BE(self._pPacketPos, id)
        self._pPacketPos = self.storeU64BE(self._pPacketPos, value)
        self._length += 12

    def end(self):
        self._pPacketPos = self.storeU32BE(self._pPacketPos, self.SMA_VERSION)
        self._pPacketPos = self.storeU32BE(self._pPacketPos, 0x01020452)
        self._length += 8

        self.storeU16BE(self._pDataSize, self._length)
        self.storeU32BE(self._pPacketPos, 0)
        self._length += 4

        self._length = self._headerLength + self._length - self.INITIAL_PAYLOAD_LENGTH
        return self._length

    def getData(self):
        return self.meterPacket

    def getLength(self):
        return self._length

    def storeU16BE(self, pPos, value):
        self.meterPacket[pPos] = (value >> 8) & 0xFF
        self.meterPacket[pPos + 1] = value & 0xFF
        return pPos + 2

    def storeU32BE(self, pPos, value):
        pPos = self.storeU16BE(pPos, (value >> 16) & 0xFFFF)
        return self.storeU16BE(pPos, value & 0xFFFF)

    def storeU64BE(self, pPos, value):
        pPos = self.storeU32BE(pPos, (value >> 32) & 0xFFFFFFFF)
        return self.storeU32BE(pPos, value & 0xFFFFFFFF)

    def offsetOf(self, pData, identifier, size):
        for i in range(size):
            if pData[i] == identifier:
                return i
        return None

    def initEmeterPacket(self, serNo):
        WLEN = 0xfa
        DSRC = 0xfb
        DTIM = 0xfc

        SMA_METER_HEADER = bytearray([
            ord('S'), ord('M'), ord('A'), 0,
            0x00, 0x04, 0x02, 0xa0, 0x00, 0x00, 0x00, 0x01,
            WLEN, WLEN, 0x00, 0x10, 0x60, 0x69,
            0x01, 0x0e, DSRC, DSRC, DSRC, DSRC,
            DTIM, DTIM, DTIM, DTIM
        ])

        self._headerLength = len(SMA_METER_HEADER)
        self.meterPacket[:self._headerLength] = SMA_METER_HEADER

        self._pDataSize = self.offsetOf(self.meterPacket, WLEN, self._headerLength)
        self._pMeterTime = self.offsetOf(self.meterPacket, DTIM, self._headerLength)

        pSerNo = self.offsetOf(self.meterPacket, DSRC, self._headerLength)
        self.storeU32BE(pSerNo, serNo)
