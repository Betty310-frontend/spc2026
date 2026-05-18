"use client";

import { useParams, useRouter } from "next/navigation";
import Image from "next/image";
import { Button, Tag, Spin, InputNumber, Divider, message } from "antd";
import { ShoppingCartOutlined, ArrowLeftOutlined, InboxOutlined } from "@ant-design/icons";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { productsApi, cartApi } from "@/lib/api";
import { useAuthStore } from "@/store/authStore";
import { Product } from "@/types";

export default function ProductDetailPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const { isLoggedIn } = useAuthStore();
  const queryClient = useQueryClient();
  const [quantity, setQuantity] = useState(1);

  const { data: product, isLoading } = useQuery<Product>({
    queryKey: ["product", id],
    queryFn: () => productsApi.detail(Number(id)).then((r) => r.data),
  });

  const addMutation = useMutation({
    mutationFn: () => cartApi.add(Number(id), quantity),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["cart"] });
      message.success(`장바구니에 ${quantity}개 담았습니다!`);
    },
    onError: () => {
      message.error("장바구니 추가에 실패했습니다.");
    },
  });

  const handleAddToCart = () => {
    if (!isLoggedIn) {
      message.warning("로그인이 필요한 서비스입니다.");
      router.push("/login");
      return;
    }
    addMutation.mutate();
  };

  if (isLoading) {
    return (
      <div className="flex justify-center py-32">
        <Spin size="large" />
      </div>
    );
  }

  if (!product) {
    return (
      <div className="text-center py-20 text-gray-500">
        <p>상품을 찾을 수 없습니다.</p>
        <Button onClick={() => router.back()} className="mt-4">
          뒤로가기
        </Button>
      </div>
    );
  }

  return (
    <div>
      <Button icon={<ArrowLeftOutlined />} onClick={() => router.back()} className="mb-6">
        목록으로
      </Button>

      <div className="bg-white rounded-2xl shadow-sm overflow-hidden">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-0">
          {/* 이미지 */}
          <div className="relative h-80 md:h-full min-h-80 bg-gray-100">
            <Image
              src={product.image_url}
              alt={product.name}
              fill
              className="object-cover"
              sizes="(max-width: 768px) 100vw, 50vw"
            />
          </div>

          {/* 상품 정보 */}
          <div className="p-8 flex flex-col">
            <Tag color="blue" className="self-start mb-3 text-sm">
              {product.category}
            </Tag>
            <h1 className="text-2xl font-bold text-gray-800 mb-3">{product.name}</h1>
            <p className="text-gray-500 leading-relaxed mb-6">{product.description}</p>

            <Divider />

            <div className="flex items-center gap-2 mb-2">
              <InboxOutlined className="text-gray-400" />
              <span className="text-gray-500 text-sm">재고: {product.stock}개</span>
            </div>
            <p className="text-3xl font-bold text-blue-600 mb-6">
              {product.price.toLocaleString()}원
            </p>

            <div className="flex items-center gap-3 mb-6">
              <span className="text-gray-600 font-medium">수량</span>
              <InputNumber
                min={1}
                max={product.stock}
                value={quantity}
                onChange={(v) => setQuantity(v ?? 1)}
                size="large"
              />
              <span className="text-gray-400 text-sm">
                합계:{" "}
                <strong className="text-gray-700">
                  {(product.price * quantity).toLocaleString()}원
                </strong>
              </span>
            </div>

            <Button
              type="primary"
              size="large"
              icon={<ShoppingCartOutlined />}
              loading={addMutation.isPending}
              onClick={handleAddToCart}
              className="w-full"
            >
              장바구니 담기
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
