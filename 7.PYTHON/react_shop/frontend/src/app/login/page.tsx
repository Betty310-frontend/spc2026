"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { Form, Input, Button, Card, message, Typography } from "antd";
import { UserOutlined, LockOutlined, ShopOutlined } from "@ant-design/icons";
import { useMutation } from "@tanstack/react-query";
import { useAuthStore } from "@/store/authStore";
import { authApi } from "@/lib/api";
import { LoginResponse } from "@/types";
import axios from "axios";

const { Title, Text } = Typography;

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuthStore();
  const [form] = Form.useForm();

  const loginMutation = useMutation({
    mutationFn: (values: { username: string; password: string }) => authApi.login(values),
    onSuccess: (res) => {
      const { token, user } = res.data as LoginResponse;
      login(token, user);
      message.success(`${user.username}님, 환영합니다!`);
      router.push("/");
    },
    onError: (err) => {
      if (axios.isAxiosError(err)) {
        message.error(err.response?.data?.error || "로그인에 실패했습니다.");
      }
    },
  });

  return (
    <div className="flex justify-center items-start pt-10">
      <Card className="w-full max-w-md shadow-md rounded-2xl">
        <div className="text-center mb-8">
          <ShopOutlined className="text-4xl text-blue-500 mb-3" />
          <Title level={3} className="!mb-1">
            로그인
          </Title>
          <Text className="text-gray-500">Shop에 오신 걸 환영합니다</Text>
        </div>

        <Form
          form={form}
          layout="vertical"
          onFinish={(values) => loginMutation.mutate(values)}
          size="large"
        >
          <Form.Item
            name="username"
            label="아이디"
            rules={[{ required: true, message: "아이디를 입력해주세요." }]}
          >
            <Input prefix={<UserOutlined />} placeholder="아이디" />
          </Form.Item>

          <Form.Item
            name="password"
            label="비밀번호"
            rules={[{ required: true, message: "비밀번호를 입력해주세요." }]}
          >
            <Input.Password prefix={<LockOutlined />} placeholder="비밀번호" />
          </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              className="w-full"
              loading={loginMutation.isPending}
            >
              로그인
            </Button>
          </Form.Item>
        </Form>

        <div className="text-center text-sm text-gray-500">
          계정이 없으신가요?{" "}
          <Link href="/register" className="text-blue-500 hover:underline font-medium">
            회원가입
          </Link>
        </div>
      </Card>
    </div>
  );
}
