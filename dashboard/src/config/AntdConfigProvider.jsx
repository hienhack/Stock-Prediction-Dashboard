import { ConfigProvider } from "antd";

function AntdConfigProvider({ children }) {
  return (
    <ConfigProvider
      theme={{
        token: {
          // colorBgContainer: "#0000",
          colorPrimary: "#cbd5e1",
        },
        components: {
          Select: {
            controlHeight: 38,
            boxShadowSecondary: "none",
          },
        },
      }}
    >
      {children}
    </ConfigProvider>
  );
}

export default AntdConfigProvider;
