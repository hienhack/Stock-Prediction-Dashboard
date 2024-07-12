import { ConfigProvider, Input } from "antd";

function Search() {
  return (
    <div className="flex space-x-2">
      <ConfigProvider
        theme={{
          components: {
            Input: {
              style: {
                borderRadius: "0.5rem",
                backgroundColor: "#1E1E1E",
                color: "#fff",
                borderColor: "#1E1E1E",
              },
            },
          },
        }}
      >
        <Input placeholder="Search..." allowClear />
      </ConfigProvider>
    </div>
  );
}

export default Search;
