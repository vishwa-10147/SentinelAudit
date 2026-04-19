
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';


import { api } from '../api';

const initialFiles = {
  scan: null,
};


  const [files, setFiles] = useState(initialFiles);
  const [company, setCompany] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [scanId, setScanId] = useState(null);
  const navigate = useNavigate();


  const handleFileChange = (e) => {
    setFiles({ ...files, scan: e.target.files[0] });
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFiles({ ...files, scan: e.dataTransfer.files[0] });
    }
  };


  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    if (!files.scan || !company) {
      setError('Scan file and company name are required.');
      return;
    }
    setSubmitting(true);
    try {
      const formData = new FormData();
      formData.append('file', files.scan);
      // Optionally add company name if backend supports it
      // formData.append('company_name', company);
      const res = await api.post('/api/scans/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setSuccess('Scan uploaded successfully!');
      setScanId(res.data.scan_id);
      setFiles(initialFiles);
      setCompany('');
      setTimeout(() => {
        navigate('/reports');
      }, 1000);
    } catch (err) {
      setError('Upload failed.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="p-8 max-w-xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Upload Scan File</h2>
      <form className="flex flex-col gap-6" onSubmit={handleSubmit}>
        <input
          className="border p-2 rounded"
          type="text"
          placeholder="Company Name"
          value={company}
          onChange={e => setCompany(e.target.value)}
          required
        />
        <div
          className="border-2 border-dashed rounded p-4 flex flex-col items-center bg-gray-50"
          onDrop={handleDrop}
          onDragOver={e => e.preventDefault()}
        >
          <label className="mb-2 font-semibold">Scan .jsonl file</label>
          <input
            type="file"
            accept="application/json,.jsonl"
            onChange={handleFileChange}
            className="mb-2"
            required={!files.scan}
          />
          {files.scan && <span className="text-green-600 text-sm">{files.scan.name}</span>}
        </div>
        <button
          className="bg-purple-600 text-white py-2 rounded hover:bg-purple-700 disabled:opacity-50"
          type="submit"
          disabled={submitting}
        >
          {submitting ? 'Uploading...' : 'Upload & Continue'}
        </button>
        {error && <div className="text-red-600 text-sm">{error}</div>}
        {success && <div className="text-green-600 text-sm">{success}</div>}
        {scanId && <div className="text-blue-600 text-sm">Scan ID: {scanId}</div>}
      </form>
    </div>
  );
