package com.deconest.order.service;

import com.deconest.cart.domain.CartItem;
import com.deconest.cart.repository.CartItemRepository;
import com.deconest.catalog.domain.Product;
import com.deconest.catalog.domain.ProductStatus;
import com.deconest.order.api.dto.CheckoutSummaryResponse;
import com.deconest.order.api.dto.CreateOrderRequest;
import com.deconest.order.api.dto.OrderItemResponse;
import com.deconest.order.api.dto.OrderResponse;
import com.deconest.order.api.dto.ShippingAddressResponse;
import com.deconest.order.domain.CustomerOrder;
import com.deconest.order.domain.OrderItem;
import com.deconest.order.domain.OrderStatus;
import com.deconest.order.domain.ShippingAddress;
import com.deconest.order.repository.CustomerOrderRepository;
import com.deconest.order.repository.OrderItemRepository;
import com.deconest.user.domain.UserAccount;
import com.deconest.user.repository.UserAccountRepository;
import jakarta.persistence.EntityNotFoundException;
import java.math.BigDecimal;
import java.time.Instant;
import java.util.List;
import java.util.UUID;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional
public class OrderService {

    private final CustomerOrderRepository customerOrderRepository;
    private final OrderItemRepository orderItemRepository;
    private final CartItemRepository cartItemRepository;
    private final UserAccountRepository userAccountRepository;

    public OrderService(
            CustomerOrderRepository customerOrderRepository,
            OrderItemRepository orderItemRepository,
            CartItemRepository cartItemRepository,
            UserAccountRepository userAccountRepository) {
        this.customerOrderRepository = customerOrderRepository;
        this.orderItemRepository = orderItemRepository;
        this.cartItemRepository = cartItemRepository;
        this.userAccountRepository = userAccountRepository;
    }

    @Transactional(readOnly = true)
    public CheckoutSummaryResponse getCheckoutSummary(String email) {
        List<CartItem> cartItems = getCartItems(email);
        validateCartItems(cartItems);
        return toCheckoutSummary(cartItems);
    }

    public OrderResponse createOrder(String email, CreateOrderRequest request) {
        UserAccount customer = getUser(email);
        List<CartItem> cartItems = getCartItems(email);
        validateCartItems(cartItems);

        BigDecimal subtotal = calculateSubtotal(cartItems);
        ShippingAddress shippingAddress = toShippingAddress(request);
        CustomerOrder order = customerOrderRepository.save(new CustomerOrder(
                customer,
                generateOrderNumber(),
                OrderStatus.PENDING_PAYMENT,
                subtotal,
                subtotal,
                shippingAddress));

        List<OrderItem> orderItems = cartItems.stream()
                .map(cartItem -> toOrderItem(order, cartItem))
                .toList();

        orderItemRepository.saveAll(orderItems);
        cartItems.forEach(cartItem -> cartItem.getProduct().reserveQuantity(cartItem.getQuantity()));
        cartItemRepository.deleteAll(cartItems);

        return toOrderResponse(order, orderItems);
    }

    @Transactional(readOnly = true)
    public List<OrderResponse> listOrders(String email) {
        return customerOrderRepository.findByCustomerEmailOrderByCreatedAtDesc(email).stream()
                .map(order -> toOrderResponse(order, orderItemRepository.findByOrderIdOrderByCreatedAtAsc(order.getId())))
                .toList();
    }

    @Transactional(readOnly = true)
    public OrderResponse getOrder(String email, Long orderId) {
        CustomerOrder order = customerOrderRepository.findByIdAndCustomerEmail(orderId, email)
                .orElseThrow(() -> new EntityNotFoundException("Order not found: " + orderId));
        List<OrderItem> items = orderItemRepository.findByOrderIdOrderByCreatedAtAsc(order.getId());
        return toOrderResponse(order, items);
    }

    private UserAccount getUser(String email) {
        return userAccountRepository.findByEmail(email)
                .orElseThrow(() -> new EntityNotFoundException("User not found with email: " + email));
    }

    private List<CartItem> getCartItems(String email) {
        List<CartItem> cartItems = cartItemRepository.findByUserEmailOrderByCreatedAtAsc(email);
        if (cartItems.isEmpty()) {
            throw new IllegalStateException("Cart is empty");
        }
        return cartItems;
    }

    private BigDecimal calculateSubtotal(List<CartItem> cartItems) {
        return cartItems.stream()
                .map(this::calculateLineTotal)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
    }

    private void validateCartItems(List<CartItem> cartItems) {
        for (CartItem cartItem : cartItems) {
            Product product = cartItem.getProduct();
            if (product.getStatus() != ProductStatus.ACTIVE) {
                throw new IllegalStateException("Product is not available for checkout: " + product.getId());
            }
            if (cartItem.getQuantity() > product.getQuantity()) {
                throw new IllegalStateException("Insufficient stock for product: " + product.getId());
            }
        }
    }

    private BigDecimal calculateLineTotal(CartItem cartItem) {
        return cartItem.getProduct().getPrice().multiply(BigDecimal.valueOf(cartItem.getQuantity()));
    }

    private ShippingAddress toShippingAddress(CreateOrderRequest request) {
        return new ShippingAddress(
                request.shippingAddress().fullName(),
                request.shippingAddress().phoneNumber(),
                request.shippingAddress().addressLine1(),
                request.shippingAddress().addressLine2(),
                request.shippingAddress().city(),
                request.shippingAddress().state(),
                request.shippingAddress().district(),
                request.shippingAddress().country(),
                request.shippingAddress().pinCode());
    }

    private OrderItem toOrderItem(CustomerOrder order, CartItem cartItem) {
        Product product = cartItem.getProduct();
        BigDecimal lineTotal = calculateLineTotal(cartItem);
        return new OrderItem(
                order,
                product,
                product.getName(),
                product.getPrice(),
                cartItem.getQuantity(),
                lineTotal);
    }

    private CheckoutSummaryResponse toCheckoutSummary(List<CartItem> cartItems) {
        List<OrderItemResponse> items = cartItems.stream()
                .map(cartItem -> new OrderItemResponse(
                        null,
                        cartItem.getProduct().getId(),
                        cartItem.getProduct().getName(),
                        cartItem.getProduct().getPrice(),
                        cartItem.getQuantity(),
                        calculateLineTotal(cartItem)))
                .toList();

        int totalItems = items.stream()
                .map(OrderItemResponse::quantity)
                .reduce(0, Integer::sum);

        BigDecimal subtotal = items.stream()
                .map(OrderItemResponse::lineTotal)
                .reduce(BigDecimal.ZERO, BigDecimal::add);

        return new CheckoutSummaryResponse(totalItems, subtotal, items);
    }

    private OrderResponse toOrderResponse(CustomerOrder order, List<OrderItem> items) {
        List<OrderItemResponse> itemResponses = items.stream()
                .map(this::toOrderItemResponse)
                .toList();

        return new OrderResponse(
                order.getId(),
                order.getOrderNumber(),
                order.getStatus(),
                order.getSubtotal(),
                order.getTotalAmount(),
                order.getCreatedAt(),
                toShippingAddressResponse(order.getShippingAddress()),
                itemResponses);
    }

    private OrderItemResponse toOrderItemResponse(OrderItem orderItem) {
        return new OrderItemResponse(
                orderItem.getId(),
                orderItem.getProduct().getId(),
                orderItem.getProductName(),
                orderItem.getUnitPrice(),
                orderItem.getQuantity(),
                orderItem.getLineTotal());
    }

    private ShippingAddressResponse toShippingAddressResponse(ShippingAddress shippingAddress) {
        return new ShippingAddressResponse(
                shippingAddress.getFullName(),
                shippingAddress.getPhoneNumber(),
                shippingAddress.getAddressLine1(),
                shippingAddress.getAddressLine2(),
                shippingAddress.getCity(),
                shippingAddress.getState(),
                shippingAddress.getDistrict(),
                shippingAddress.getCountry(),
                shippingAddress.getPinCode());
    }

    private String generateOrderNumber() {
        String token = UUID.randomUUID().toString().replace("-", "").substring(0, 12).toUpperCase();
        return "DN-" + Instant.now().toEpochMilli() + "-" + token;
    }
}
