import { useState } from 'react';

export default function EpisodeList({ episodes, onSelectContent }) {
  const [expandedEpisode, setExpandedEpisode] = useState(null);

  const toggleEpisode = (episodeId) => {
    setExpandedEpisode(expandedEpisode === episodeId ? null : episodeId);
  };

  return (
    <div className="w-80 h-screen bg-gray-50 border-r border-gray-200 overflow-y-auto">
      <div className="p-4 bg-blue-600 text-white sticky top-0">
        <h1 className="text-xl font-bold">Economics U$A</h1>
        <p className="text-sm opacity-90">Spanish Resources</p>
      </div>

      <div className="divide-y divide-gray-200">
        {episodes.map((episode) => (
          <div key={episode.id} className="border-b border-gray-200">
            <button
              onClick={() => toggleEpisode(episode.id)}
              className="w-full px-4 py-3 text-left hover:bg-gray-100 transition-colors flex items-center justify-between group"
            >
              <div>
                <div className="font-semibold text-gray-900">
                  {episode.number}. {episode.title}
                </div>
                <div className="text-xs text-gray-500 mt-1">
                  {episode.contents.length} files
                </div>
              </div>
              <svg
                className={`w-5 h-5 text-gray-400 group-hover:text-gray-600 transition-transform ${
                  expandedEpisode === episode.id ? 'rotate-180' : ''
                }`}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            {expandedEpisode === episode.id && (
              <div className="bg-white border-t border-gray-100">
                {episode.contents.map((content, idx) => (
                  <button
                    key={idx}
                    onClick={() => onSelectContent(content)}
                    className="w-full px-6 py-2.5 text-left hover:bg-blue-50 transition-colors text-sm border-b border-gray-50 last:border-0 flex items-center gap-2"
                  >
                    {content.format === 'pdf' ? (
                      <svg className="w-4 h-4 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M4 18h12V6h-4V2H4v16zm-2 1V0h10l4 4v15H2z"/>
                        <text x="6" y="14" fontSize="8" fill="currentColor" fontWeight="bold">PDF</text>
                      </svg>
                    ) : (
                      <svg className="w-4 h-4 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z"/>
                      </svg>
                    )}
                    <span className="text-gray-700">{content.label}</span>
                  </button>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* RSS Feed Links */}
      <div className="border-t border-gray-300 bg-gray-100 p-4 space-y-2">
        <h3 className="text-sm font-semibold text-gray-700 mb-2">Subscribe to Audio Feeds</h3>
        <a
          href="/economics-usa-video-spanish.rss"
          className="flex items-center gap-2 px-3 py-2 bg-white border border-gray-200 rounded hover:bg-blue-50 transition-colors text-sm"
          target="_blank"
          rel="noopener noreferrer"
        >
          <svg className="w-4 h-4 text-orange-500" fill="currentColor" viewBox="0 0 20 20">
            <path d="M5 3a1 1 0 000 2c5.523 0 10 4.477 10 10a1 1 0 102 0C17 8.373 11.627 3 5 3z"/>
            <path d="M4 9a1 1 0 011-1 7 7 0 017 7 1 1 0 11-2 0 5 5 0 00-5-5 1 1 0 01-1-1zM3 15a2 2 0 114 0 2 2 0 01-4 0z"/>
          </svg>
          <span className="text-gray-700">Video Audio RSS</span>
        </a>
        <a
          href="/economics-usa-audio-spanish.rss"
          className="flex items-center gap-2 px-3 py-2 bg-white border border-gray-200 rounded hover:bg-blue-50 transition-colors text-sm"
          target="_blank"
          rel="noopener noreferrer"
        >
          <svg className="w-4 h-4 text-orange-500" fill="currentColor" viewBox="0 0 20 20">
            <path d="M5 3a1 1 0 000 2c5.523 0 10 4.477 10 10a1 1 0 102 0C17 8.373 11.627 3 5 3z"/>
            <path d="M4 9a1 1 0 011-1 7 7 0 017 7 1 1 0 11-2 0 5 5 0 00-5-5 1 1 0 01-1-1zM3 15a2 2 0 114 0 2 2 0 01-4 0z"/>
          </svg>
          <span className="text-gray-700">Audio Program RSS</span>
        </a>
      </div>
    </div>
  );
}
