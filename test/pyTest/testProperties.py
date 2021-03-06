import os

# Check if environment is setup to run the tests
if os.environ.get('AVTRANSCODER_TEST_AUDIO_WAVE_FILE') is None:
	from nose.plugins.skip import SkipTest
	raise SkipTest("Need to define environment variable AVTRANSCODER_TEST_AUDIO_WAVE_FILE")

from nose.tools import *

from pyAvTranscoder import avtranscoder as av

av.preloadCodecsAndFormats()
av.Logger.setLogLevel(av.AV_LOG_QUIET)


def testAddMetadataDate():
	"""
	Add metadata 'date' to the outputFile.
	"""
	outputFileName = "testAddMetadataDate.wav"

	ouputFile = av.OutputFile( outputFileName )
	transcoder = av.Transcoder( ouputFile )

	# rewrap a stream
	transcoder.add( os.environ['AVTRANSCODER_TEST_AUDIO_WAVE_FILE'], 0, "")

	# add one metadata
	metadata_to_check = ("date", "value")
	ouputFile.addMetadata( metadata_to_check[0], metadata_to_check[1] )

	progress = av.NoDisplayProgress()
	transcoder.process( progress )

	inputFile = av.InputFile( outputFileName )
	inputFile.analyse( progress, av.eAnalyseLevelHeader )
	properties = inputFile.getProperties()

	assert_in( metadata_to_check, properties.getMetadatas() )

def testAddImpossibleMetadata():
	"""
	Can't add an impossible metadata to the outputFile.
	"""
	outputFileName = "testAddMetadataPlop.wav"

	ouputFile = av.OutputFile( outputFileName )
	transcoder = av.Transcoder( ouputFile )

	# rewrap a stream
	transcoder.add( os.environ['AVTRANSCODER_TEST_AUDIO_WAVE_FILE'], 0, "")

	# add one metadata
	metadata_to_check = ("undefinedMetadataKey", "undefinedMetadataValue")
	ouputFile.addMetadata( metadata_to_check[0], metadata_to_check[1] )

	progress = av.NoDisplayProgress()
	transcoder.process( progress )

	inputFile = av.InputFile( outputFileName )
	inputFile.analyse( progress, av.eAnalyseLevelHeader )
	properties = inputFile.getProperties()

	assert_not_in( metadata_to_check, properties.getMetadatas() )

