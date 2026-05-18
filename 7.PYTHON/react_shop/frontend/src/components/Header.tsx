"use client";

import { useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Badge, Button, Dropdown, Space, message } from "antd";
import {
  ShoppingCartOutlined,
  LogoutOutlined,
  LoginOutlined,
  ShopOutlined,
  DownOutlined,
} from "@ant-design/icons";
import { useQuery } from "@tanstack/react-query";
import { useAuthStore } from "@/store/authStore";
import { cartApi } from "@/lib/api";
import type { MenuProps } from "antd";

export default function Header() {
  const router = useRouter();
  const { isLoggedIn, user, logout, initFromStorage } = useAuthStore();

  useEffect(() => {
    initFromStorage();
  }, [initFromStorage]);

  const { data: cartData } = useQuery({
    queryKey: ["cart"],
    queryFn: () => cartApi.get().then((r) => r.data),
    enabled: isLoggedIn,
    staleTime: 0,
  });

  const handleLogout = () => {
    logout();
    message.success("로그아웃되었습니다.");
    router.push("/");
  };

  const userMenuItems: MenuProps["items"] = [
    {
      key: "username",
      label: <span className="font-semibold">{user?.username}님</span>,
      disabled: true,
    },
    { type: "divider" },
    {
      key: "logout",
      label: "로그아웃",
      icon: <LogoutOutlined />,
      onClick: handleLogout,
    },
  ];

  return (
    <header className="sticky top-0 z-50 bg-white shadow-sm">
      <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        {/* 로고 */}
        <Link
          href="/"
          className="flex items-center gap-2 text-xl font-bold text-blue-600 hover:text-blue-700"
        >
          <ShopOutlined />
          <span>Shop</span>
        </Link>

        {/* 우측 메뉴 */}
        <Space size="middle">
          {/* 장바구니 */}
          {isLoggedIn && (
            <Link href="/cart">
              <Badge count={cartData?.count ?? 0} showZero={false}>
                <Button icon={<ShoppingCartOutlined />} size="large">
                  장바구니
                </Button>
              </Badge>
            </Link>
          )}

          {/* 로그인 / 유저 메뉴 */}
          {isLoggedIn ? (
            <Dropdown menu={{ items: userMenuItems }} placement="bottomRight">
              <a onClick={(e) => e.preventDefault()}>
                <Space>
                  {user?.username}
                  <DownOutlined />
                </Space>
              </a>
            </Dropdown>
          ) : (
            <Space>
              <Link href="/login">
                <Button icon={<LoginOutlined />} type="primary">
                  로그인
                </Button>
              </Link>
              <Link href="/register">
                <Button>회원가입</Button>
              </Link>
            </Space>
          )}
        </Space>
      </div>
    </header>
  );
}
