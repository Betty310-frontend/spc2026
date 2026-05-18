"use client";

import Image from "next/image";
import Link from "next/link";
import { Card, Button, Tag, message } from "antd";
import { ShoppingCartOutlined } from "@ant-design/icons";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useAuthStore } from "@/store/authStore";
import { cartApi } from "@/lib/api";
import { Product } from "@/types";
import { useRouter } from "next/navigation";

interface Props {
  product: Product;
}

export default function ProductCard({ product }: Props) {
  const router = useRouter();
  const { isLoggedIn } = useAuthStore();
  const queryClient = useQueryClient();

  const addMutation = useMutation({
    mutationFn: () => cartApi.add(product.id, 1),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["cart"] });
      message.success("장바구니에 담았습니다!");
    },
    onError: () => {
      message.error("장바구니 추가에 실패했습니다.");
    },
  });

  const handleAddToCart = (e: React.MouseEvent) => {
    e.preventDefault();
    if (!isLoggedIn) {
      message.warning("로그인이 필요한 서비스입니다.");
      router.push("/login");
      return;
    }
    addMutation.mutate();
  };

  return (
    <Link href={`/products/${product.id}`}>
      <Card
        hoverable
        className="h-full flex flex-col"
        cover={
          <div className="relative h-52 overflow-hidden bg-gray-100">
            <Image
              src={product.image_url}
              alt={product.name}
              fill
              className="object-cover"
              sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 25vw"
            />
          </div>
        }
        actions={[
          <Button
            key="cart"
            type="primary"
            icon={<ShoppingCartOutlined />}
            loading={addMutation.isPending}
            onClick={handleAddToCart}
            className="w-[90%] mx-2"
          >
            장바구니 담기
          </Button>,
        ]}
      >
        <Card.Meta
          title={<span className="text-base font-semibold line-clamp-1">{product.name}</span>}
          description={
            <div className="flex flex-col h-28 justify-between">
              <div className="flex flex-col gap-1.5 items-start">
                <Tag color="blue">{product.category}</Tag>
                <p className="text-gray-500 text-sm line-clamp-2">{product.description}</p>
              </div>
              <div>
                <p className="text-lg font-bold text-blue-600">
                  {product.price.toLocaleString()}원
                </p>
                <p className="text-xs text-gray-400">재고 {product.stock}개</p>
              </div>
            </div>
          }
        />
      </Card>
    </Link>
  );
}
