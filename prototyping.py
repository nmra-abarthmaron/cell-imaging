import cellprofiler_core.pipeline
import cellprofiler_core.preferences
import cellprofiler_core.utilities.java
import pathlib

    
if __name__ == "__main__":
    
    # Replacement config class, to circumvent the default wx-based GUI class
    cellprofiler_core.preferences.set_headless()

    # Start java VM
    cellprofiler_core.utilities.java.start_java()

    # Load pipeline, for this prototype we'll use 'soma_image'
    pipeline = cellprofiler_core.pipeline.Pipeline()