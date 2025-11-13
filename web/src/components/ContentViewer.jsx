import PdfViewer from './PdfViewer';
import AudioPlayer from './AudioPlayer';

export default function ContentViewer({ content }) {
  if (!content) {
    return (
      <div className="flex-1 flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <svg className="w-24 h-24 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <h2 className="text-xl font-semibold text-gray-700 mb-2">
            Select a file to view
          </h2>
          <p className="text-gray-500">
            Choose an episode and content from the sidebar
          </p>
        </div>
      </div>
    );
  }

  // Use the path directly from episodes.json (already has leading slash)
  const filePath = content.path;

  return (
    <div className="flex-1 flex flex-col">
      {/* Content Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <h2 className="text-lg font-semibold text-gray-900">
          {content.label}
        </h2>
        <p className="text-sm text-gray-500 mt-1">
          {content.fileName}
        </p>
      </div>

      {/* Content Display */}
      {content.format === 'pdf' ? (
        <PdfViewer filePath={filePath} />
      ) : (
        <AudioPlayer filePath={filePath} />
      )}
    </div>
  );
}
