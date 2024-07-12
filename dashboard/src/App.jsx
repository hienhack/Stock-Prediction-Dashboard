import Search from "./components/Search";

function App() {
  return (
    <div className="h-screen bg-indigo-950 py-10">
      <div className="w-4/5 max-w-screen-2xl h-full mx-auto">
        <h1 className="text-3xl font-medium text-slate-200 mt-2.5">
          Microsoft
        </h1>
        <div className="flex justify-between items-end mt-3">
          <Search />
        </div>
      </div>
    </div>
  );
}

export default App;
