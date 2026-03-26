package com.deconest.user.api;

import com.deconest.user.api.dto.CreateUserRequest;
import com.deconest.user.api.dto.DeliveryAgentProfileResponse;
import com.deconest.user.api.dto.SellerProfileResponse;
import com.deconest.user.api.dto.UpdateDeliveryAgentProfileRequest;
import com.deconest.user.api.dto.UpdateSellerProfileRequest;
import com.deconest.user.api.dto.UpdateUserProfileRequest;
import com.deconest.user.api.dto.UserAccountResponse;
import com.deconest.user.api.dto.UserProfileResponse;
import com.deconest.user.service.UserService;
import jakarta.validation.Valid;
import java.util.List;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping
    public List<UserAccountResponse> listUsers() {
        return userService.listUsers();
    }

    @GetMapping("/{id}")
    public UserAccountResponse getUser(@PathVariable Long id) {
        return userService.getUser(id);
    }

    @PostMapping
    public UserAccountResponse createUser(@Valid @RequestBody CreateUserRequest request) {
        return userService.createUser(request);
    }

    @GetMapping("/me/profile")
    public UserProfileResponse getCurrentUserProfile(Authentication authentication) {
        return userService.getCurrentUserProfile(authentication.getName());
    }

    @PutMapping("/me/profile")
    public UserProfileResponse updateCurrentUserProfile(
            Authentication authentication,
            @Valid @RequestBody UpdateUserProfileRequest request) {
        return userService.updateCurrentUserProfile(authentication.getName(), request);
    }

    @GetMapping("/me/seller-profile")
    public SellerProfileResponse getCurrentSellerProfile(Authentication authentication) {
        return userService.getCurrentSellerProfile(authentication.getName());
    }

    @PutMapping("/me/seller-profile")
    public SellerProfileResponse updateCurrentSellerProfile(
            Authentication authentication,
            @Valid @RequestBody UpdateSellerProfileRequest request) {
        return userService.updateCurrentSellerProfile(authentication.getName(), request);
    }

    @GetMapping("/me/delivery-profile")
    public DeliveryAgentProfileResponse getCurrentDeliveryAgentProfile(Authentication authentication) {
        return userService.getCurrentDeliveryAgentProfile(authentication.getName());
    }

    @PutMapping("/me/delivery-profile")
    public DeliveryAgentProfileResponse updateCurrentDeliveryAgentProfile(
            Authentication authentication,
            @Valid @RequestBody UpdateDeliveryAgentProfileRequest request) {
        return userService.updateCurrentDeliveryAgentProfile(authentication.getName(), request);
    }
}
