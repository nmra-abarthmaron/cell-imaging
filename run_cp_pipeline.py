import cellprofiler_core.pipeline
import cellprofiler_core.preferences
import cellprofiler_core.utilities.java
    
def run_cp_pipeline(data_path, pipeline_file):

    # Replacement config class, to circumvent the default wx-based GUI class
    cellprofiler_core.preferences.set_headless()       

    # Start java VM
    cellprofiler_core.utilities.java.start_java()
    
    # Set default output directory
    analysis_name = pipeline_file.name[:-len('.cppipe')]
    save_dir = data_path.parent / analysis_name
    if not save_dir.exists():
        save_dir.mkdir(parents=True)
    cellprofiler_core.preferences.set_default_output_directory(save_dir)

    # Open a pipeline
    pipeline = cellprofiler_core.pipeline.Pipeline()
    pipeline.load(pipeline_file)

    # Get image file list
    file_list = list(data_path.glob('*.tif'))
    files = [file.as_uri() for file in file_list]
    pipeline.read_file_list(files)

    # Change the name of the spreadsheet export
    # Note - assumes 'ExportToSpreadsheet' is last module in the cp pipeline
    pipeline.modules()[-1].settings()[16].set_value(analysis_name + '_')

    # Run the pipeline
    output_measurements = pipeline.run()

    # Stop java VM
    cellprofiler_core.utilities.java.stop_java()

    # Report completion
    print(analysis_name + ' analysis complete')

    return save_dir