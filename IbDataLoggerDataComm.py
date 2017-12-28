import sys
import socket
import io
import json
import avro.datafile
import avro.schema
import avro.io
import SharedVars
import IbDataLoggerEnums
import IbDataLoggerUtilities

def SerializeObject(dataObject, schema):
	try:
		AvroSerializationBuffer = io.BytesIO()
		ReturnBuffer = bytes()
		writer = avro.datafile.DataFileWriter(AvroSerializationBuffer, avro.io.DatumWriter(), schema)
		writer.append(dataObject)
		writer.flush()
		AvroSerializationBuffer.seek(0)
		ReturnBuffer = AvroSerializationBuffer.getvalue()
		AvroSerializationBuffer.close()
		return True, ReturnBuffer
	except Exception as e:
		AvroSerializationBuffer.close()
		IbDataLoggerUtilities.LogError('Exception in SerializeObect: ' + str(e))
		return False, 0

def TcpExchange(BufferToSend, SessionTypeName, PacketTaskName, ExpectedSessionTypeName, ExpectedPacketTaskName):
	try:
		PacketLengthBuffer = (16 + len(BufferToSend)).to_bytes(8, byteorder='little')
		SessionTypeBuffer = (IbDataLoggerEnums.SessionType[SessionTypeName].value).to_bytes(4, byteorder='little')
		PacketTaskBuffer = (IbDataLoggerEnums.PacketTask[PacketTaskName].value).to_bytes(4, byteorder='little')
		OutgoingBuffer = PacketLengthBuffer + SessionTypeBuffer + PacketTaskBuffer + BufferToSend
		# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# s.connect((SharedVars.IbDataLinkIpAddress, SharedVars.IbDataLinkIpPortNumber))
		s = socket.create_connection((SharedVars.IbDataLinkIpAddress, SharedVars.IbDataLinkIpPortNumber), timeout=SharedVars.SocketTimeout)
		s.send(OutgoingBuffer)
		ExpectedSessionTypeInt = IbDataLoggerEnums.SessionType[ExpectedSessionTypeName].value
		ExpectedPacketTaskInt = IbDataLoggerEnums.PacketTask[ExpectedPacketTaskName].value
		EntirePacketLength = int.from_bytes(s.recv(8), byteorder='little')
		ReceivedSessionTypeInt = int.from_bytes(s.recv(4), byteorder='little')
		ReceivedPacketTaskInt = int.from_bytes(s.recv(4), byteorder='little')
		if ReceivedSessionTypeInt != ExpectedSessionTypeInt:
			IbDataLoggerUtilities.LogError('In TcpExchange expected session type ' + ExpectedSessionTypeName + ' but received ' + IbDataLoggerEnums.SessionType(ReceivedSessionTypeInt).name)
		if ReceivedPacketTaskInt != ExpectedPacketTaskInt:
			IbDataLoggerUtilities.LogError('In TcpExchange expected packet task ' + ExpectedPacketTaskName + ' but received ' + IbDataLoggerEnums.PacketTask(ReceivedPacketTaskInt).name)
		DataPacketLength = EntirePacketLength - 8 - 4 - 4
		GotTheWholePacket = False
		IncomingPacket = bytes()
		while not GotTheWholePacket:
			NextPacketPiece = s.recv(10000)
			IncomingPacket = IncomingPacket + NextPacketPiece
			if len(IncomingPacket) >= DataPacketLength:
				GotTheWholePacket = True
		s.close()
		return True, IncomingPacket
	except Exception as e:
		IbDataLoggerUtilities.LogError('Exception in TcpExchange: ' + str(e))
		try:
			s.close()
		except:
			pass
		return False, 0

def DeserializeObject(stream):
	try:
		returnObject = {}
		ByteBufferAvro = io.BytesIO(stream)
		ByteBufferAvro.seek(0)
		reader = avro.datafile.DataFileReader(ByteBufferAvro, avro.io.DatumReader())
		for datum in reader:
			returnObject = datum
		ByteBufferAvro.close()
		reader.close()
		return True, returnObject
	except Exception as e:
		ByteBufferAvro.close()
		reader.close()
		IbDataLoggerUtilities.LogError('Exception in DeserializeObect: ' + str(e))
		return False, 0

