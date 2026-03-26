package com.deconest.user.service;

import com.deconest.common.security.PasswordHasher;
import com.deconest.user.api.dto.CreateUserRequest;
import com.deconest.user.api.dto.DeliveryAgentProfileResponse;
import com.deconest.user.api.dto.SellerProfileResponse;
import com.deconest.user.api.dto.UpdateDeliveryAgentProfileRequest;
import com.deconest.user.api.dto.UpdateSellerProfileRequest;
import com.deconest.user.api.dto.UpdateUserProfileRequest;
import com.deconest.user.api.dto.UserAccountResponse;
import com.deconest.user.api.dto.UserProfileResponse;
import com.deconest.user.domain.DeliveryAgentProfile;
import com.deconest.user.domain.SellerProfile;
import com.deconest.user.domain.UserAccount;
import com.deconest.user.domain.UserProfile;
import com.deconest.user.domain.UserRole;
import com.deconest.user.repository.DeliveryAgentProfileRepository;
import com.deconest.user.repository.SellerProfileRepository;
import com.deconest.user.repository.UserAccountRepository;
import com.deconest.user.repository.UserProfileRepository;
import jakarta.persistence.EntityExistsException;
import jakarta.persistence.EntityNotFoundException;
import java.util.List;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional
public class UserService {

    private final UserAccountRepository userAccountRepository;
    private final UserProfileRepository userProfileRepository;
    private final SellerProfileRepository sellerProfileRepository;
    private final DeliveryAgentProfileRepository deliveryAgentProfileRepository;
    private final PasswordHasher passwordHasher;

    public UserService(
            UserAccountRepository userAccountRepository,
            UserProfileRepository userProfileRepository,
            SellerProfileRepository sellerProfileRepository,
            DeliveryAgentProfileRepository deliveryAgentProfileRepository,
            PasswordHasher passwordHasher) {
        this.userAccountRepository = userAccountRepository;
        this.userProfileRepository = userProfileRepository;
        this.sellerProfileRepository = sellerProfileRepository;
        this.deliveryAgentProfileRepository = deliveryAgentProfileRepository;
        this.passwordHasher = passwordHasher;
    }

    public UserAccountResponse createUser(CreateUserRequest request) {
        if (userAccountRepository.existsByEmail(request.email())) {
            throw new EntityExistsException("User already exists with email: " + request.email());
        }

        UserAccount userAccount = new UserAccount(
                request.email(),
                request.fullName(),
                passwordHasher.hash(request.password()),
                request.role());

        UserAccount saved = userAccountRepository.save(userAccount);
        provisionDefaultProfile(saved);
        return toResponse(saved);
    }

    @Transactional(readOnly = true)
    public List<UserAccountResponse> listUsers() {
        return userAccountRepository.findAll().stream()
                .map(this::toResponse)
                .toList();
    }

    @Transactional(readOnly = true)
    public UserAccountResponse getUser(Long id) {
        UserAccount account = userAccountRepository.findById(id)
                .orElseThrow(() -> new EntityNotFoundException("User not found: " + id));
        return toResponse(account);
    }

    @Transactional(readOnly = true)
    public UserAccountResponse getUserByEmail(String email) {
        UserAccount account = userAccountRepository.findByEmail(email)
                .orElseThrow(() -> new EntityNotFoundException("User not found with email: " + email));
        return toResponse(account);
    }

    @Transactional(readOnly = true)
    public UserProfileResponse getCurrentUserProfile(String email) {
        UserProfile profile = userProfileRepository.findByUserEmail(email)
                .orElseThrow(() -> new EntityNotFoundException("User profile not found for email: " + email));
        return toResponse(profile);
    }

    public UserProfileResponse updateCurrentUserProfile(String email, UpdateUserProfileRequest request) {
        UserProfile profile = userProfileRepository.findByUserEmail(email)
                .orElseThrow(() -> new EntityNotFoundException("User profile not found for email: " + email));
        profile.updateProfile(
                request.country(),
                request.state(),
                request.city(),
                request.district(),
                request.addressLine1(),
                request.addressLine2(),
                request.phoneNumber(),
                request.alternatePhoneNumber(),
                request.pinCode());
        return toResponse(profile);
    }

    @Transactional(readOnly = true)
    public SellerProfileResponse getCurrentSellerProfile(String email) {
        SellerProfile profile = sellerProfileRepository.findByUserEmail(email)
                .orElseThrow(() -> new EntityNotFoundException("Seller profile not found for email: " + email));
        return toResponse(profile);
    }

    public SellerProfileResponse updateCurrentSellerProfile(String email, UpdateSellerProfileRequest request) {
        SellerProfile profile = sellerProfileRepository.findByUserEmail(email)
                .orElseThrow(() -> new EntityNotFoundException("Seller profile not found for email: " + email));
        profile.updateProfile(
                request.ownerName(),
                request.gstNumber(),
                request.panNumber(),
                request.mapLocation(),
                request.phoneNumber(),
                request.alternatePhoneNumber());
        return toResponse(profile);
    }

    @Transactional(readOnly = true)
    public DeliveryAgentProfileResponse getCurrentDeliveryAgentProfile(String email) {
        DeliveryAgentProfile profile = deliveryAgentProfileRepository.findByUserEmail(email)
                .orElseThrow(() -> new EntityNotFoundException("Delivery agent profile not found for email: " + email));
        return toResponse(profile);
    }

    public DeliveryAgentProfileResponse updateCurrentDeliveryAgentProfile(
            String email,
            UpdateDeliveryAgentProfileRequest request) {
        DeliveryAgentProfile profile = deliveryAgentProfileRepository.findByUserEmail(email)
                .orElseThrow(() -> new EntityNotFoundException("Delivery agent profile not found for email: " + email));
        profile.updateProfile(
                request.firstName(),
                request.lastName(),
                request.phoneNumber(),
                request.pinCode(),
                request.bankName(),
                request.accountHolderName(),
                request.accountNumber(),
                request.routingNumber(),
                request.maxDeliveryDistanceKm(),
                request.insuranceExpiryDate());
        return toResponse(profile);
    }

    private void provisionDefaultProfile(UserAccount userAccount) {
        if (userAccount.getRole() == UserRole.SELLER) {
            sellerProfileRepository.save(new SellerProfile(userAccount));
            return;
        }

        if (userAccount.getRole() == UserRole.DELIVERY_AGENT) {
            deliveryAgentProfileRepository.save(new DeliveryAgentProfile(userAccount));
            return;
        }

        userProfileRepository.save(new UserProfile(userAccount));
    }

    private UserAccountResponse toResponse(UserAccount userAccount) {
        return new UserAccountResponse(
                userAccount.getId(),
                userAccount.getEmail(),
                userAccount.getFullName(),
                userAccount.getRole(),
                userAccount.isActive(),
                userAccount.isVerified(),
                userAccount.isBlacklisted());
    }

    private UserProfileResponse toResponse(UserProfile profile) {
        UserAccount user = profile.getUser();
        return new UserProfileResponse(
                user.getId(),
                user.getEmail(),
                user.getFullName(),
                profile.getCountry(),
                profile.getState(),
                profile.getCity(),
                profile.getDistrict(),
                profile.getAddressLine1(),
                profile.getAddressLine2(),
                profile.getPhoneNumber(),
                profile.getAlternatePhoneNumber(),
                profile.getPinCode());
    }

    private SellerProfileResponse toResponse(SellerProfile profile) {
        UserAccount user = profile.getUser();
        return new SellerProfileResponse(
                user.getId(),
                user.getEmail(),
                user.getFullName(),
                profile.getOwnerName(),
                profile.getGstNumber(),
                profile.getPanNumber(),
                profile.getMapLocation(),
                profile.getPhoneNumber(),
                profile.getAlternatePhoneNumber());
    }

    private DeliveryAgentProfileResponse toResponse(DeliveryAgentProfile profile) {
        UserAccount user = profile.getUser();
        return new DeliveryAgentProfileResponse(
                user.getId(),
                user.getEmail(),
                user.getFullName(),
                profile.getFirstName(),
                profile.getLastName(),
                profile.getPhoneNumber(),
                profile.getPinCode(),
                profile.getBankName(),
                profile.getAccountHolderName(),
                profile.getAccountNumber(),
                profile.getRoutingNumber(),
                profile.getMaxDeliveryDistanceKm(),
                profile.getInsuranceExpiryDate(),
                profile.isApproved(),
                profile.isRejected());
    }
}
