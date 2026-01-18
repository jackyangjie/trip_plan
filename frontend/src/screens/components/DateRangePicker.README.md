# DateRangePicker 组件使用说明

## 概述

DateRangePicker 是一个精美的日期范围选择器组件，用于旅行规划应用中。它包含一个自定义的日期选择器模态框，提供流畅的用户体验和优美的视觉效果。

## 功能特性

- ✅ 可视化的日期选择器模态框
- ✅ 年、月、日选择
- ✅ 日期验证（结束日期不能早于开始日期）
- ✅ 日期格式化显示（中文格式：YYYY年MM月DD日）
- ✅ 错误提示和视觉反馈
- ✅ 符合 Material Design 3 规范
- ✅ 主题集成（使用项目的主题颜色）
- ✅ 移动端友好的触摸目标

## 组件 API

### DateRangePicker

```typescript
interface DateRangePickerProps {
  startDate: string;              // 开始日期 (YYYY-MM-DD)
  endDate: string;                // 结束日期 (YYYY-MM-DD)
  onStartDateChange: (date: string) => void;  // 开始日期变更回调
  onEndDateChange: (date: string) => void;    // 结束日期变更回调
  error?: string;                 // 可选的外部错误消息
}
```

### DateModalPicker

```typescript
interface DateModalPickerProps {
  visible: boolean;               // 是否显示模态框
  initialDate: string;            // 初始日期 (YYYY-MM-DD)
  onDismiss: () => void;           // 关闭模态框回调
  onConfirm: (date: string) => void;  // 确认日期回调
  minDate?: string;                // 可选的最小日期
  maxDate?: string;                // 可选的最大日期
}
```

## 使用示例

```typescript
import React, { useState } from 'react';
import DateRangePicker from './DateRangePicker';

function MyComponent() {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  return (
    <DateRangePicker
      startDate={startDate}
      endDate={endDate}
      onStartDateChange={setStartDate}
      onEndDateChange={setEndDate}
    />
  );
}
```

## 验证规则

1. 开始日期不能早于今天
2. 结束日期必须晚于开始日期
3. 结束日期不能与开始日期相同
4. 如果开始日期被更新为晚于结束日期，结束日期会被清空

## 视觉特性

- 主题色：深海洋蓝 (#1A5490)
- 强调色：温暖的日落橙 (#E6A157)
- 次要强调色：青色 (#00BFA5)
- 圆角：12px (MD3 标准)
- 阴影：符合 Material Design 规范
- 触摸目标：最小 48px (无障碍标准)

## 日期格式

- 输入格式：YYYY-MM-DD (ISO 8601)
- 显示格式：YYYY年MM月DD日 (中文)

## 依赖项

- React Native
- React Native Paper
- react-native-vector-icons
- dayjs
