"use client";

import { useState } from "react";
import { Input, Select, Pagination, Empty, Spin, Tag } from "antd";
import { SearchOutlined } from "@ant-design/icons";
import { useQuery } from "@tanstack/react-query";
import ProductCard from "@/components/ProductCard";
import { productsApi } from "@/lib/api";
import { ProductListResponse } from "@/types";

const { Search } = Input;

export default function Home() {
  const [page, setPage] = useState(1);
  const [keyword, setKeyword] = useState("");
  const [category, setCategory] = useState("");

  const { data: categoriesData } = useQuery({
    queryKey: ["categories"],
    queryFn: () => productsApi.categories().then((r) => r.data),
  });

  const { data, isLoading } = useQuery<ProductListResponse>({
    queryKey: ["products", page, keyword, category],
    queryFn: () =>
      productsApi
        .list({ page, per_page: 8, keyword: keyword || undefined, category: category || undefined })
        .then((r) => r.data),
  });

  const handleSearch = (value: string) => {
    setKeyword(value);
    setPage(1);
  };

  const handleCategory = (value: string) => {
    setCategory(value);
    setPage(1);
  };

  return (
    <div>
      {/* 페이지 제목 */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-1">🛍️ 상품 목록</h1>
        <p className="text-gray-500">다양한 상품을 만나보세요</p>
      </div>

      {/* 필터 영역 */}
      <div className="flex flex-col sm:flex-row gap-3 mb-6">
        <Search
          placeholder="상품명 검색"
          enterButton={<SearchOutlined />}
          size="large"
          onSearch={handleSearch}
          allowClear
          className="flex-1"
        />
        <Select
          placeholder="카테고리"
          size="large"
          style={{ minWidth: 150 }}
          allowClear
          onChange={handleCategory}
          options={[
            { label: "전체", value: "" },
            ...(categoriesData?.categories?.map((c: string) => ({ label: c, value: c })) ?? []),
          ]}
        />
      </div>

      {/* 검색 결과 요약 */}
      {data && (
        <div className="mb-4 text-sm text-gray-500">
          총 <span className="font-semibold text-gray-800">{data.total}</span>개 상품
          {category && (
            <Tag color="blue" className="ml-2">
              {category}
            </Tag>
          )}
          {keyword && (
            <Tag color="orange" className="ml-1">
              &ldquo;{keyword}&rdquo;
            </Tag>
          )}
        </div>
      )}

      {/* 상품 그리드 */}
      {isLoading ? (
        <div className="flex justify-center py-20">
          <Spin size="large" />
        </div>
      ) : data?.products?.length === 0 ? (
        <Empty description="상품이 없습니다." className="py-20" />
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5">
          {data?.products?.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      )}

      {/* 페이지네이션 */}
      {data && data.total > 8 && (
        <div className="flex justify-center mt-8">
          <Pagination
            current={page}
            total={data.total}
            pageSize={8}
            onChange={setPage}
            showSizeChanger={false}
          />
        </div>
      )}
    </div>
  );
}
