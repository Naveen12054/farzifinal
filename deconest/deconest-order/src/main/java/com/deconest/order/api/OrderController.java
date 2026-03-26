package com.deconest.order.api;

import com.deconest.order.api.dto.CheckoutSummaryResponse;
import com.deconest.order.api.dto.CreateOrderRequest;
import com.deconest.order.api.dto.OrderResponse;
import com.deconest.order.service.OrderService;
import jakarta.validation.Valid;
import java.util.List;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/orders")
public class OrderController {

    private final OrderService orderService;

    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }

    @GetMapping("/checkout")
    public CheckoutSummaryResponse getCheckoutSummary(Authentication authentication) {
        return orderService.getCheckoutSummary(authentication.getName());
    }

    @PostMapping
    public OrderResponse createOrder(
            Authentication authentication,
            @Valid @RequestBody CreateOrderRequest request) {
        return orderService.createOrder(authentication.getName(), request);
    }

    @GetMapping
    public List<OrderResponse> listOrders(Authentication authentication) {
        return orderService.listOrders(authentication.getName());
    }

    @GetMapping("/{orderId}")
    public OrderResponse getOrder(Authentication authentication, @PathVariable Long orderId) {
        return orderService.getOrder(authentication.getName(), orderId);
    }
}
