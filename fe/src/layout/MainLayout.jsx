import React from 'react';
import { Breadcrumb, Typography, Layout, theme } from 'antd';
import { Outlet } from 'react-router'

const { Content } = Layout;

const MainLayout = () => {
    const { token: { colorBgContainer, borderRadiusLG } } = theme.useToken();
    const { Title } = Typography
    return (
        <Layout style={{ height: "100vh" }}>
            <Content style={{ padding: '0 48px',flex: 1 }}>
                <Breadcrumb
                    style={{ margin: '16px 0 5px 0' }}
                    items={[{ title: <Title level={3}>Chat Bot</Title> }]}
                />
                <div
                    style={{
                        padding: 24,
                        height: "87.5%",
                        background: colorBgContainer,
                        borderRadius: borderRadiusLG,
                    }}
                >
                    <Outlet/>
                </div>
            </Content>
        </Layout>
    );
};
export default MainLayout;