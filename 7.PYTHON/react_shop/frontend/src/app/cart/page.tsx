"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import Image from "next/image";
import {
  Button,
  InputNumber,
  Table,
  Popconfirm,
  Empty,
  Spin,
  message,
  Typography,
  Divider,
} from "antd";
import { DeleteOutlined, ShoppingOutlined, ClearOutlined } from "@ant-design/icons";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useAuthStore } from "@/store/authStore";
import { cartApi } from "@/lib/api";
import { CartItem, CartResponse } from "@/types";
import type { ColumnsType } from "antd/es/table";

const { Title, Text } = Typography;

export default function CartPage() {
  const router = useRouter();
  const { isLoggedIn, initFromStorage } = useAuthStore();
  const queryClient = useQueryClient();

  useEffect(() => {
    initFromStorage();
  }, [initFromStorage]);

  useEffect(() => {
    if (!isLoggedIn) {
      router.push("/login");
    }
  }, [isLoggedIn, router]);

  const { data, isLoading } = useQuery<CartResponse>({
    queryKey: ["cart"],
    queryFn: () => cartApi.get().then((r) => r.data),
    enabled: isLoggedIn,
  });

  const updateMutation = useMutation({
    mutationFn: ({ cart_id, quantity }: { cart_id: number; quantity: number }) =>
      cartApi.update(cart_id, quantity),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["cart"] }),
    onError: () => message.error("수량 수정에 실패했습니다."),
  });

  const removeMutation = useMutation({
    mutationFn: (cart_id: number) => cartApi.remove(cart_id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["cart"] });
      message.success("상품을 삭제했습니다.");
    },
  });

  const clearMutation = useMutation({
    mutationFn: () => cartApi.clear(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["cart"] });
      message.success("장바구니를 비웠습니다.");
    },
  });

  const columns: ColumnsType<CartItem> = [
    {
      title: "상품",
      key: "product",
      render: (_, item) => (
        <div className="flex items-center gap-3">
          <div className="relative w-16 h-16 rounded-lg overflow-hidden bg-gray-100 flex-shrink-0">
            <Image
              src={item.image_url}
              alt={item.name}
              fill
              className="object-cover"
              sizes="64px"
            />
          </div>
          <div>
            <p className="font-medium text-gray-800 line-clamp-1">{item.name}</p>
            <p className="text-sm text-gray-400">{item.category}</p>
          </div>
        </div>
      ),
    },
    {
      title: "단가",
      dataIndex: "price",
      align: "right",
      render: (price: number) => <span className="font-medium">{price.toLocaleString()}원</span>,
    },
    {
      title: "수량",
      dataIndex: "quantity",
      align: "center",
      render: (qty: number, item) => (
        <InputNumber
          min={1}
          max={item.stock}
          value={qty}
          onChange={(v) => {
            if (v && v !== qty) {
              updateMutation.mutate({ cart_id: item.id, quantity: v });
            }
          }}
          size="small"
          style={{ width: 70 }}
        />
      ),
    },
    {
      title: "합계",
      align: "right",
      render: (_, item) => (
        <span className="font-bold text-blue-600">
          {(item.price * item.quantity).toLocaleString()}원
        </span>
      ),
    },
    {
      title: "",
      align: "center",
      render: (_, item) => (
        <Popconfirm
          title="이 상품을 삭제할까요?"
          onConfirm={() => removeMutation.mutate(item.id)}
          okText="삭제"
          cancelText="취소"
        >
          <Button type="text" danger icon={<DeleteOutlined />} loading={removeMutation.isPending} />
        </Popconfirm>
      ),
    },
  ];

  if (!isLoggedIn) return null;

  if (isLoading) {
    return (
      <div className="flex justify-center py-32">
        <Spin size="large" />
      </div>
    );
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <Title level={3} className="!mb-0">
          🛒 장바구니
        </Title>
        {data && data.count > 0 && (
          <Popconfirm
            title="장바구니를 모두 비울까요?"
            onConfirm={() => clearMutation.mutate()}
            okText="비우기"
            cancelText="취소"
          >
            <Button danger icon={<ClearOutlined />} loading={clearMutation.isPending}>
              전체 삭제
            </Button>
          </Popconfirm>
        )}
      </div>

      {data?.count === 0 ? (
        <div className="bg-white rounded-2xl shadow-sm py-20">
          <Empty description="장바구니가 비어 있습니다." image={Empty.PRESENTED_IMAGE_SIMPLE}>
            <Button type="primary" onClick={() => router.push("/")} icon={<ShoppingOutlined />}>
              쇼핑 계속하기
            </Button>
          </Empty>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* 상품 목록 */}
          <div className="lg:col-span-2 bg-white rounded-2xl shadow-sm overflow-hidden">
            <Table
              columns={columns}
              dataSource={data?.items}
              rowKey="id"
              pagination={false}
              scroll={{ x: true }}
            />
          </div>

          {/* 결제 요약 */}
          <div className="bg-white rounded-2xl shadow-sm p-6 h-fit">
            <Title level={5}>주문 요약</Title>
            <Divider />
            <div className="space-y-3">
              <div className="flex justify-between text-gray-600">
                <span>상품 수</span>
                <span>{data?.count}종</span>
              </div>
              <div className="flex justify-between text-gray-600">
                <span>상품 금액</span>
                <span>{data?.total_price.toLocaleString()}원</span>
              </div>
              <div className="flex justify-between text-gray-600">
                <span>배송비</span>
                <span className="text-green-600">무료</span>
              </div>
            </div>
            <Divider />
            <div className="flex justify-between items-center mb-6">
              <Text strong className="text-lg">
                총 결제 금액
              </Text>
              <Text strong className="text-xl text-blue-600">
                {data?.total_price.toLocaleString()}원
              </Text>
            </div>
            <Button type="primary" size="large" className="w-full">
              결제하기
            </Button>
            <Button className="w-full mt-2" onClick={() => router.push("/")}>
              쇼핑 계속하기
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
