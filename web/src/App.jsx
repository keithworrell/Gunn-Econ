import { useState } from 'react';
import EpisodeList from './components/EpisodeList';
import ContentViewer from './components/ContentViewer';
import episodesData from './data/episodes.json';

function App() {
  const [selectedContent, setSelectedContent] = useState(null);

  return (
    <div className="flex h-screen overflow-hidden">
      <EpisodeList
        episodes={episodesData}
        onSelectContent={setSelectedContent}
      />
      <ContentViewer content={selectedContent} />
    </div>
  );
}

export default App;
