import cellprofiler_core.pipeline
import cellprofiler_core.preferences
import cellprofiler_core.utilities.java
import cellprofiler
import pathlib
    
#if __name__ == "__main__":

# Experiment name
exp_name = '220811 96w 9 Gene KO '
#exp_name = '220810 96w Dye Chem Controls/'

# Analysis run name & date
analysis_date = '2022-08-16'
#analysis_name = 'soma_image'
analysis_name = 'soma_objects'
#analysis_name = 'neurite_segment'

# CP pipeline file
#pipeline_file = '/home/ubuntu/cell-imaging/cellprofiler_pipelines/2022-08-16_soma_image.cppipe'
pipeline_file = '/home/ubuntu/cell-imaging/cellprofiler_pipelines/2022-08-16_soma_objects.cppipe'
#pipeline_file = '/home/ubuntu/cell-imaging/cellprofiler_pipelines/2022-08-16_neurite_segment.cppipe'

# Replacement config class, to circumvent the default wx-based GUI class
cellprofiler_core.preferences.set_headless()

# Start java VM
cellprofiler_core.utilities.java.start_java()

# Load pipeline, for this prototype we'll use 'soma_image'
pipeline = cellprofiler_core.pipeline.Pipeline()

# Open a pipeline
pipeline = cellprofiler_core.pipeline.Pipeline()
pipeline.load(pipeline_file)

# Set default output directory
save_dir = pathlib.Path('/fsx/processed-data') / exp_name / analysis_date / analysis_name

# Create save dir if it doesn't exist
if not save_dir.exists():
    save_dir.mkdir(parents=True)

cellprofiler_core.preferences.set_default_output_directory(save_dir)

# Set image file list
data_dir = pathlib.Path('/fsx/processed-data') / exp_name / 'max_projections'

file_list = list(data_dir.glob('*.tif'))
files = [file.as_uri() for file in file_list]
pipeline.read_file_list(files)

# Change the name of the spreadsheet export
pipeline.modules()[10].settings()[16].set_value(
    analysis_date + '_' + 
    analysis_name + '_'
)

# Applicable to soma objects analysis only. should be done in cppipe file
pipeline.modules()[10].settings()[4].set_value('yes')
pipeline.modules()[10].settings()[5].set_value('yes')

# Run the pipeline
output_measurements = pipeline.run()

# Stop java VM
cellprofiler_core.utilities.java.stop_java()


print(analysis_name + ' analysis complete')