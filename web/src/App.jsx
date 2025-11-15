import { useState } from 'react';
import EpisodeList from './components/EpisodeList';
import ContentViewer from './components/ContentViewer';
import episodesData from './data/episodes.json';

function App() {
  const [selectedContent, setSelectedContent] = useState(null);

  return (
    <div className="flex h-screen overflow-hidden flex-col">
      <div className="flex flex-1 overflow-hidden">
        <EpisodeList
          episodes={episodesData}
          onSelectContent={setSelectedContent}
        />
        <ContentViewer content={selectedContent} />
      </div>
      <div className="bg-gray-800 text-gray-300 text-xs py-2 px-4 text-center border-t border-gray-700">
        Provided for fair use and academic accessibility purposes only. No warranty is provided. Use at your own discretion.
      </div>
    </div>
  );
}

export default App;
