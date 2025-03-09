'use client';
import React, { useState, useEffect } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";

function Assessment() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [resumeUploaded, setResumeUploaded] = useState(false);
  const [resumeFileName, setResumeFileName] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Fetch assessment data when component mounts
    const fetchAssessmentData = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/assessments/current', {
          credentials: 'include'
        });
        if (response.status === 404) {
          // Handle case when no assessment exists
          setError('No active assessment found. Please start a new assessment.');
          return;
        }
        if (!response.ok) {
          throw new Error('Failed to fetch assessment data');
        }
        const data = await response.json();
        if (data.resume_file_path) {
          setResumeUploaded(true);
          setResumeFileName(data.resume_file_path.split('/').pop());
        }
      } catch (error) {
        console.error('Error fetching assessment data:', error);
        setError('Unable to load assessment data. Please try again later.');
      }
    };

    fetchAssessmentData();
  }, []);

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      if (file.type === 'application/pdf') {
        setSelectedFile(file);
        await handleUpload(file);
      } else {
        alert('Please upload a PDF file only');
      }
    }
  };

  const handleDrop = async (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    if (file) {
      if (file.type === 'application/pdf') {
        setSelectedFile(file);
        await handleUpload(file);
      } else {
        alert('Please upload a PDF file only');
      }
    }
  };

  const handleUpload = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/api/assessment/upload-resume', {
        method: 'POST',
        body: formData,
        credentials: 'include'
      });

      if (response.ok) {
        const data = await response.json();
        setResumeUploaded(true);
        setResumeFileName(file.name);
      } else {
        const errorData = await response.json();
        alert(errorData.detail || 'Failed to upload resume');
      }
    } catch (error) {
      console.error('Error uploading resume:', error);
      alert('Error uploading resume');
    }
  };

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold mb-4">Personality Assessment</h2>
      {error && (
        <div className="bg-red-50 text-red-600 p-4 rounded-lg mb-4">
          {error}
        </div>
      )}
      <div className="space-y-4">
        <p className="text-gray-600">
          Welcome to your personality assessment section. Here you can:
        </p>
        <ul className="list-disc pl-5 space-y-2 text-gray-600">
          <li>Take new personality assessments</li>
          <li>View your previous assessment results</li>
          <li>Track your personality development over time</li>
        </ul>
        <div className="mt-6">
          {resumeUploaded ? (
            <div className="space-y-4">
              <div className="p-4 bg-gray-50 rounded-lg">
                <p className="text-sm text-gray-600">Uploaded Resume:</p>
                <p className="font-medium">{resumeFileName}</p>
              </div>
              <Button variant="default" size="lg">
                Start Assessment
              </Button>
            </div>
          ) : (
            <Dialog>
              <DialogTrigger asChild>
                <Button variant="default" size="lg">
                  Start New Assessment
                </Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Upload Your Resume</DialogTitle>
                </DialogHeader>
                <div
                  className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center"
                  onDrop={handleDrop}
                  onDragOver={handleDragOver}
                >
                  <input
                    type="file"
                    accept=".pdf"
                    onChange={handleFileChange}
                    className="hidden"
                    id="resume-upload"
                  />
                  <label
                    htmlFor="resume-upload"
                    className="cursor-pointer text-blue-600 hover:text-blue-700"
                  >
                    Click to upload
                  </label>
                  <p className="text-sm text-gray-500 mt-2">
                    or drag and drop your PDF file here
                  </p>
                  {selectedFile && (
                    <div className="mt-4 text-sm text-green-600">
                      Selected file: {selectedFile.name}
                    </div>
                  )}
                </div>
              </DialogContent>
            </Dialog>
          )}
        </div>
      </div>
    </div>
  );
}

export default Assessment;