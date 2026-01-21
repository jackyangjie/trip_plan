from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class TripStatus(str, Enum):
    planning = "planning"
    confirmed = "confirmed"
    completed = "completed"
    cancelled = "cancelled"


class AgentType(str, Enum):
    planner = "planner"
    transport = "transport"
    accommodation = "accommodation"
    attraction = "attraction"
    food = "food"
    budget = "budget"


class SessionStatus(str, Enum):
    active = "active"
    completed = "completed"


class DayBudget(BaseModel):
    """单日预算模型"""

    total: int = Field(..., ge=0, description="当天总预算（元）")
    transport: int = Field(0, ge=0, description="当天交通费用（元）")
    accommodation: int = Field(0, ge=0, description="当天住宿费用（元）")
    food: int = Field(0, ge=0, description="当天餐饮费用（元）")
    activities: int = Field(0, ge=0, description="当天活动门票费用（元）")


class TripBudget(BaseModel):
    """旅行预算模型，包含预算和实际花费"""

    total_budget: int = Field(..., ge=0, description="总预算（元）")
    total_spent: int = Field(0, ge=0, description="总花费（元）")
    transport_spent: int = Field(0, ge=0, description="交通实际花费（元）")
    accommodation_spent: int = Field(0, ge=0, description="住宿实际花费（元）")
    food_spent: int = Field(0, ge=0, description="餐饮实际花费（元）")
    activities_spent: int = Field(0, ge=0, description="活动门票实际花费（元）")


class User(BaseModel):
    """用户信息模型"""

    id: str = Field(..., description="用户唯一标识")
    email: str = Field(..., description="用户邮箱")
    nickname: Optional[str] = Field(None, description="用户昵称")
    preferences: dict = Field(default_factory=dict, description="用户偏好设置")


class Trip(BaseModel):
    """旅行计划基础模型"""

    id: Optional[str] = Field(None, description="旅行计划唯一标识")
    user_id: Optional[str] = Field(None, description="关联的用户ID")
    title: str = Field(..., description="旅行标题")
    destinations: List[str] = Field(..., description="目的地列表")
    start_date: str = Field(..., description="开始日期 (YYYY-MM-DD)")
    end_date: str = Field(..., description="结束日期 (YYYY-MM-DD)")
    budget: TripBudget = Field(..., description="旅行预算")
    status: TripStatus = Field(TripStatus.planning, description="旅行状态")
    itinerary: List[dict] = Field(default_factory=list, description="行程安排列表")
    share_token: Optional[str] = Field(None, description="分享令牌")
    is_public: bool = Field(False, description="是否公开")


class TripCreate(BaseModel):
    """创建旅行计划请求模型"""

    title: str = Field(..., description="旅行标题")
    destinations: List[str] = Field(..., description="目的地列表")
    start_date: str = Field(..., description="开始日期 (YYYY-MM-DD)")
    end_date: str = Field(..., description="结束日期 (YYYY-MM-DD)")
    budget: TripBudget = Field(..., description="旅行预算")
    travelers: int = Field(2, ge=1, le=20, description="旅行人数")
    preferences: dict = Field(default_factory=dict, description="用户偏好设置")


# ============== 景点信息模型 ==============


class Attraction(BaseModel):
    """景点信息模型，包含景点的详细信息"""

    id: Optional[str] = Field(None, description="景点唯一标识")
    name: str = Field(..., description="景点名称")
    description: Optional[str] = Field(None, description="景点描述")
    location: dict = Field(..., description="位置信息 (name, lat, lng, address)")
    category: Optional[str] = Field(
        None, description="景点类型 (自然风光/历史古迹/主题公园等)"
    )
    rating: Optional[float] = Field(None, ge=0, le=5, description="景点评分 (0-5)")
    ticket_price: Optional[int] = Field(None, ge=0, description="票价 (元)")
    opening_hours: Optional[str] = Field(None, description="开放时间")
    recommended_duration: Optional[int] = Field(
        None, ge=0, description="建议游玩时长 (分钟)"
    )
    image_url: Optional[str] = Field(None, description="景点图片URL")
    tags: List[str] = Field(default_factory=list, description="标签 (必去/亲子/拍照等)")
    best_visit_time: Optional[str] = Field(None, description="最佳游玩时间")
    tips: Optional[str] = Field(None, description="游玩提示")


# ============== 交通信息模型 ==============


class Transport(BaseModel):
    """交通信息模型，支持多种交通方式"""

    id: Optional[str] = Field(None, description="交通方案唯一标识")
    type: str = Field(
        ..., description="交通类型 (flight/train/bus/car/taxi/metro/walk)"
    )
    from_location: dict = Field(..., description="出发地 (name, lat, lng, address)")
    to_location: dict = Field(..., description="目的地 (name, lat, lng, address)")
    departure_time: Optional[str] = Field(None, description="出发时间")
    arrival_time: Optional[str] = Field(None, description="到达时间")
    duration: Optional[int] = Field(None, ge=0, description="时长 (分钟)")
    price: Optional[int] = Field(None, ge=0, description="价格 (元)")
    provider: Optional[str] = Field(None, description="提供商 (航空公司/高铁等)")
    details: Optional[dict] = Field(None, description="额外详情 (航班号/车次等)")
    booking_url: Optional[str] = Field(None, description="预订链接")
    notes: Optional[str] = Field(None, description="备注信息")


# ============== 酒店信息模型 ==============


class Hotel(BaseModel):
    """酒店信息模型，包含住宿详情"""

    id: Optional[str] = Field(None, description="酒店唯一标识")
    name: str = Field(..., description="酒店名称")
    location: dict = Field(..., description="位置信息 (name, lat, lng, address)")
    star_rating: Optional[int] = Field(None, ge=1, le=5, description="星级 (1-5)")
    room_type: Optional[str] = Field(None, description="房型 (标准间/大床房等)")
    price_per_night: Optional[int] = Field(None, ge=0, description="每晚价格 (元)")
    rating: Optional[float] = Field(None, ge=0, le=5, description="用户评分 (0-5)")
    amenities: List[str] = Field(
        default_factory=list, description="设施 (WiFi/空调/泳池等)"
    )
    check_in_time: Optional[str] = Field(None, description="入住时间")
    check_out_time: Optional[str] = Field(None, description="退房时间")
    image_url: Optional[str] = Field(None, description="酒店图片URL")
    description: Optional[str] = Field(None, description="酒店描述")
    contact: Optional[dict] = Field(None, description="联系方式 (phone, website)")
    distance_to_attractions: Optional[List[dict]] = Field(
        None, description="到景点距离列表"
    )


# ============== 美食信息模型 ==============


class Food(BaseModel):
    """美食/餐厅信息模型，包含餐厅和菜品详情"""

    id: Optional[str] = Field(None, description="餐厅唯一标识")
    name: str = Field(..., description="餐厅名称")
    type: str = Field(..., description="类型 (餐厅/小吃摊/咖啡厅等)")
    cuisine: Optional[str] = Field(None, description="菜系 (川菜/粤菜/日料等)")
    location: dict = Field(..., description="位置信息 (name, lat, lng, address)")
    rating: Optional[float] = Field(None, ge=0, le=5, description="评分 (0-5)")
    price_range: Optional[str] = Field(None, description="价格区间 (便宜/中等/昂贵)")
    avg_price_per_person: Optional[int] = Field(None, ge=0, description="人均消费 (元)")
    signature_dishes: List[str] = Field(default_factory=list, description="招牌菜")
    opening_hours: Optional[str] = Field(None, description="营业时间")
    image_url: Optional[str] = Field(None, description="餐厅图片URL")
    description: Optional[str] = Field(None, description="餐厅描述")
    tags: List[str] = Field(
        default_factory=list, description="标签 (网红店/老字号/必吃等)"
    )
    tips: Optional[str] = Field(None, description="用餐提示")
    contact: Optional[dict] = Field(None, description="联系方式 (phone, website)")


# ============== 天气信息模型 ==============


class Weather(BaseModel):
    """天气信息模型，包含当日天气详情"""

    location: str = Field(..., description="地点名称")
    date: str = Field(..., description="日期 (YYYY-MM-DD)")
    temperature_min: int = Field(..., description="最低温度 (摄氏度)")
    temperature_max: int = Field(..., description="最高温度 (摄氏度)")
    weather_condition: str = Field(..., description="天气状况 (晴天/多云/雨天等)")
    weather_icon: Optional[str] = Field(None, description="天气图标URL")
    humidity: Optional[int] = Field(None, ge=0, le=100, description="湿度 (%)")
    wind_speed: Optional[int] = Field(None, ge=0, description="风速 (km/h)")
    precipitation: Optional[int] = Field(None, ge=0, description="降水量 (mm)")
    tips: Optional[str] = Field(None, description="穿衣/出行建议")


class ItineraryItem(BaseModel):
    """行程项，详细描述每个时间点的活动"""

    id: Optional[str] = Field(None, description="行程项唯一标识")
    day: int = Field(..., ge=1, description="行程天数")
    time: str = Field(..., description="时间点")
    type: str = Field(
        ..., description="活动类型 (transport/accommodation/attraction/food/custom)"
    )
    title: str = Field(..., description="活动标题")
    description: Optional[str] = Field(None, description="活动描述")
    location: Optional[dict] = Field(
        None, description="位置信息 (name, lat, lng, address)"
    )
    cost: Optional[int] = Field(None, ge=0, description="费用 (元)")
    duration: Optional[int] = Field(None, ge=0, description="时长 (分钟)")
    notes: Optional[str] = Field(None, description="备注")
    data: Optional[dict] = Field(None, description="附加数据")


class DayPlan(BaseModel):
    """单日旅行计划，包含当天的所有安排"""

    day: int = Field(..., ge=1, description="行程天数")
    date: str = Field(..., description="日期 (YYYY-MM-DD)")
    budget: DayBudget = Field(..., description="当天预算")
    attractions: List[Attraction] = Field(
        default_factory=list, description="当天推荐的景点"
    )
    transports: List[Transport] = Field(
        default_factory=list, description="当天使用的交通方案"
    )
    hotel: Optional[Hotel] = Field(None, description="当天入住的酒店")
    foods: List[Food] = Field(default_factory=list, description="当天推荐的美食/餐厅")
    weather: Optional[Weather] = Field(None, description="当天天气信息")
    itinerary: List[ItineraryItem] = Field(
        default_factory=list, description="当天的详细行程安排"
    )


class DetailedTripPlan(BaseModel):
    """详细旅行计划模型，按天组织的完整旅行方案"""

    id: Optional[str] = Field(None, description="旅行计划唯一标识")
    user_id: Optional[str] = Field(None, description="关联的用户ID")
    title: str = Field(..., description="旅行标题")
    destinations: List[str] = Field(..., description="目的地列表")
    start_date: str = Field(..., description="开始日期 (YYYY-MM-DD)")
    end_date: str = Field(..., description="结束日期 (YYYY-MM-DD)")
    travelers: int = Field(2, ge=1, le=20, description="旅行人数")
    budget: TripBudget = Field(..., description="旅行总预算和花费")
    status: TripStatus = Field(TripStatus.planning, description="旅行状态")

    days: List[DayPlan] = Field(default_factory=list, description="按天组织的旅行计划")

    share_token: Optional[str] = Field(None, description="分享令牌")
    is_public: bool = Field(False, description="是否公开")
    created_at: Optional[str] = Field(None, description="创建时间")
    updated_at: Optional[str] = Field(None, description="更新时间")
