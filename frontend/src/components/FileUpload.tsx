import React, { useState, useCallback, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import { fetchPrinters, Printer } from '../api/printers';
import { motion } from 'framer-motion';

const FileUpload: React.FC = () => {
    const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
    const [gerberFile, setGerberFile] = useState<File | null>(null);
    const [drillFile, setDrillFile] = useState<File | null>(null);
    const [printers, setPrinters] = useState<Record<string, Printer>>({});
    const [imageUrl, setImageUrl] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [progress, setProgress] = useState<number>(0);
    const [error, setError] = useState<string | null>(null);
    const [selectedPrinter, setSelectedPrinter] = useState<string>(() => {
      const savedPrinterId = localStorage.getItem('selectedPrinter');
      return savedPrinterId || '';
    });
    const [flipX, setFlipX] = useState<boolean>(() => {
      return localStorage.getItem('flipX') === 'true';
    });
    
    const [flipY, setFlipY] = useState<boolean>(() => {
      return localStorage.getItem('flipY') === 'true';
    });

  useEffect(() => {
    async function loadPrinters() {
      try {
        const data = await fetchPrinters();
        setPrinters(data);
        if (!selectedPrinter) {
          const firstPrinterId = Object.keys(data)[0];
          setSelectedPrinter(firstPrinterId);
        }
      } catch (err) {
        console.error('Error loading printers:', err);
      }
    }
    loadPrinters();
  }, [selectedPrinter]);

  useEffect(() => {
    if (selectedPrinter) {
      localStorage.setItem('selectedPrinter', selectedPrinter);
    }
  }, [selectedPrinter]);
  
  useEffect(() => {
    localStorage.setItem('flipX', String(flipX));
  }, [flipX]);
  
  useEffect(() => {
    localStorage.setItem('flipY', String(flipY));
  }, [flipY]);
  

  const onDropGerber = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setGerberFile(acceptedFiles[0]);
    }
  }, []);

  const onDropDrill = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setDrillFile(acceptedFiles[0]);
    }
  }, []);

  const { getRootProps: getRootPropsGerber, getInputProps: getInputPropsGerber, isDragActive: isDragActiveGerber } = useDropzone({ onDrop: onDropGerber });
  const { getRootProps: getRootPropsDrill, getInputProps: getInputPropsDrill, isDragActive: isDragActiveDrill } = useDropzone({ onDrop: onDropDrill });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!gerberFile || !drillFile) {
      setError('Please select both files.');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      setProgress(0);

      const formData = new FormData();
      formData.append('gerber_file', gerberFile);
      formData.append('drill_file', drillFile);
      formData.append('printer_id', selectedPrinter);
      formData.append('flip_horizontal', String(flipX));
      formData.append('flip_vertical', String(flipY));


      const xhr = new XMLHttpRequest();
      xhr.open('POST', `${API_URL}/api/convert`);
      xhr.responseType = 'blob';

      xhr.upload.onprogress = (event) => {
        if (event.lengthComputable) {
          const percent = Math.round((event.loaded * 100) / event.total);
          setProgress(percent);
        }
      };

      xhr.onload = () => {
        if (xhr.status === 200) {
          const blob = new Blob([xhr.response], { type: 'image/png' });
          const url = URL.createObjectURL(blob);
          setImageUrl(url);
        } else {
          try {
            const errorData = JSON.parse(xhr.responseText);
            setError(errorData.detail || 'Server error.');
          } catch {
            setError('Server error.');
          }
        }
        setLoading(false);
      };

      xhr.onerror = () => {
        setError('Network error.');
        setLoading(false);
      };

      xhr.send(formData);

    } catch (err) {
      console.error(err);
      setError('Error loading files.');
      setLoading(false);
    }
  };

  const handleReset = () => {
    setGerberFile(null);
    setDrillFile(null);
    setImageUrl(null);
    setError(null);
    setProgress(0);
  };

  return (
    <div className="flex flex-col items-center justify-center p-4 w-full">
      <div className="bg-white shadow-md rounded-lg p-8 w-full max-w-md">
        <h1 className="text-2xl font-bold mb-6 text-center">Gerber + Drill → PNG</h1>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">

          {/* Выбор принтера */}
          {Object.keys(printers).length > 0 && (
            <div>
              <label className="block text-sm font-medium mb-1">Select printer:</label>
              <select
                value={selectedPrinter}
                onChange={(e) => setSelectedPrinter(e.target.value)}
                className="w-full border border-gray-300 rounded px-3 py-2"
              >
                {Object.entries(printers).map(([id, printer]) => (
                  <option key={id} value={id}>
                    {printer.web_name}
                  </option>
                ))}
              </select>
            </div>
          )}

          <div className="flex flex-col gap-4">
            {/* Flip X */}
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-800">Flip horizontal</span>
              <button
                type="button"
                className={`w-12 h-6 flex items-center rounded-full p-1 duration-300 ease-in-out transition-colors
                  ${flipX ? 'bg-blue-500' : 'bg-gray-300'}`}
                onClick={() => setFlipX(!flipX)}
              >
                <div
                  className={`w-4 h-4 rounded-full shadow-md transform duration-300 ease-in-out transition-transform
                    ${flipX ? 'translate-x-6 bg-white' : 'bg-white'}`}
                ></div>
              </button>
            </div>

            {/* Flip Y */}
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-800">Flip vertical</span>
              <button
                type="button"
                className={`w-12 h-6 flex items-center rounded-full p-1 duration-300 ease-in-out transition-colors
                  ${flipY ? 'bg-blue-500' : 'bg-gray-300'}`}
                onClick={() => setFlipY(!flipY)}
              >
                <div
                  className={`w-4 h-4 rounded-full shadow-md transform duration-300 ease-in-out transition-transform
                    ${flipY ? 'translate-x-6 bg-white' : 'bg-white'}`}
                ></div>
              </button>
            </div>
          </div>


          {/* Gerber file load zone */}
          <div {...getRootPropsGerber()} className={`flex flex-col items-center justify-center border-2 border-dashed rounded-lg p-8 cursor-pointer transition ${isDragActiveGerber ? 'border-blue-500 bg-blue-50' : 'border-gray-300 bg-white'}`}>
            <input {...getInputPropsGerber()} />
            <img src="/icons/gerber-file.png" alt="Gerber file" className="w-16 h-16 mb-4" />
            {gerberFile ? (
              <p className="text-green-600 text-center break-words">{gerberFile.name}</p>
            ) : (
              <p className="text-gray-500 text-center">Drag and drop Gerber (.gbr) file here or click</p>
            )}
          </div>

          {/* Drill file load zone */}
          <div {...getRootPropsDrill()} className={`flex flex-col items-center justify-center border-2 border-dashed rounded-lg p-8 cursor-pointer transition ${isDragActiveDrill ? 'border-blue-500 bg-blue-50' : 'border-gray-300 bg-white'}`}>
            <input {...getInputPropsDrill()} />
            <img src="/icons/drill-file.png" alt="Drill file" className="w-16 h-16 mb-4" />
            {drillFile ? (
              <p className="text-green-600 text-center break-words">{drillFile.name}</p>
            ) : (
              <p className="text-gray-500 text-center">Drag and drop Drill (.drl) file here or click</p>
            )}
          </div>

          {/* errors */}
          {error && <p className="text-red-500 text-sm text-center">{error}</p>}

          {/* Progress */}
          {loading && (
            <div className="w-full bg-gray-200 rounded-full h-2.5 mt-2">
              <div className="bg-blue-600 h-2.5 rounded-full transition-all" style={{ width: `${progress}%` }} />
            </div>
          )}

          {/* Buttons */}
          <div className="flex gap-2">
            <button
              type="submit"
              disabled={loading}
              className="flex-1 bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition disabled:opacity-50"
            >
              {loading ? 'Loading...' : 'Send'}
            </button>

            <button
              type="button"
              onClick={handleReset}
              className="flex-1 bg-gray-300 text-gray-700 py-2 rounded hover:bg-gray-400 transition"
            >
              Clear
            </button>
          </div>
        </form>

        {/* Image preview */}
        {imageUrl && (
          <div className="mt-6">
            <h2 className="text-lg font-semibold mb-2">Result:</h2>
            <motion.img
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5 }}
              src={imageUrl}
              alt="Result"
              className="w-full rounded shadow"
            />
            <a href={imageUrl} download={gerberFile ? gerberFile.name.replace('.gbr', '.png') : 'result.png'} className="block text-center mt-4 bg-green-500 text-white py-2 rounded hover:bg-green-600 transition">
              Download PNG
            </a>
          </div>
        )}
      </div>
    </div>
  );
};

export default FileUpload;
