# Claude AI Assistant - CareerHub Project

## 📋 **Project Overview**
CareerHub is a modern professional profile management platform built with Next.js 15, React Hook Form, and FastAPI. This document serves as a guide for Claude AI assistants working on this project.

## 🎯 **Key Project Files & Resources**

### **📚 Documentation & Best Practices**
- **`docs/frontend/REACT_FORM_RESEARCH.md`** - **CRITICAL**: Contains 2025 React Form handling best practices, solutions to common issues, and implementation patterns. **ALWAYS REFER TO THIS FILE** when working with forms.

### **🏗️ Architecture**
- **Frontend**: Next.js 15 with App Router, TypeScript, Tailwind CSS v4, shadcn/ui
- **Backend**: FastAPI with PostgreSQL, Redis, JWT authentication
- **Form Handling**: React Hook Form with FormProvider architecture (2025 best practices)

## 🚀 **Modern 2025 Patterns Implemented**

### **✅ Form Handling Best Practices**
Based on `docs/frontend/REACT_FORM_RESEARCH.md`, we use:

```typescript
// ✅ WORKING: Modern 2025 React Hook Form configuration
const methods = useForm({
  mode: 'onChange',
  triggerMode: 'onChange', // ✅ FIXES re-render issues
  reValidateMode: 'onChange',
  shouldFocusError: true,
  shouldUnregister: false,
  criteriaMode: 'firstError'
});

// ✅ FormProvider architecture (eliminates prop drilling)
<FormProvider {...methods}>
  <StepComponents /> {/* No props needed */}
</FormProvider>

// ✅ useFieldArray for dynamic arrays
const { fields, append, remove, update } = useFieldArray({
  control,
  name: 'experiences'
});
```

## 📁 **Key Directory Structure**
```
frontend/src/
├── components/
│   ├── profile/
│   │   ├── ProfileWizardSteps.tsx    # Main wizard with FormProvider
│   │   └── steps/                    # Individual wizard steps
│   ├── layout/
│   │   ├── TopBar.tsx               # Navigation with ProfileDropdown
│   │   └── ProfileDropdown.tsx      # User profile menu
│   └── ui/                          # shadcn/ui components
├── contexts/
│   └── auth-context.tsx             # Authentication state
└── hooks/
    └── use-profile.ts               # Profile management hooks
```

## 🔧 **Development Guidelines**

### **Form Development Rules**
1. **ALWAYS** use FormProvider architecture (see REACT_FORM_RESEARCH.md)
2. **NEVER** use prop drilling for form data
3. **ALWAYS** use useFieldArray for dynamic arrays
4. **ALWAYS** use Controller for complex components
5. **ALWAYS** use triggerMode: "onChange" for proper re-renders

### **Component Patterns**
```typescript
// ✅ CORRECT: Modern 2025 pattern
export function StepComponent() {
  const { control, register, formState: { errors } } = useFormContext();
  const { fields, append, remove } = useFieldArray({ control, name: 'items' });
  // ... implementation
}

// ❌ WRONG: Legacy pattern (don't use)
export function StepComponent({ register, setValue, watch, errors }) {
  // ... implementation
}
```

## 🎯 **Current Status**

### **✅ Completed Features**
- ✅ Authentication system (JWT + Refresh tokens)
- ✅ Profile creation wizard (5 steps)
- ✅ Modern form handling with React Hook Form 2025 patterns
- ✅ Profile dropdown in TopBar
- ✅ Auto-save with debouncing
- ✅ Real-time validation with Zod

### **🔄 In Progress**
- 🔄 Experience management CRUD interface
- 🔄 Project management interface
- 🔄 Skills management interface

### **📋 TODO**
- ⏳ CV generation and PDF export
- ⏳ Public profile viewing interface
- ⏳ Advanced profile features

## 🚨 **Important Notes**

### **Critical Files to Reference**
1. **`docs/frontend/REACT_FORM_RESEARCH.md`** - Form handling best practices
2. **`frontend/src/components/profile/ProfileWizardSteps.tsx`** - Main wizard implementation
3. **`frontend/src/contexts/auth-context.tsx`** - Authentication state management

### **Common Issues & Solutions**
- **Checkbox not working**: Use `triggerMode: "onChange"` in useForm config
- **Form not re-rendering**: Use FormProvider + Controller components
- **Prop drilling**: Use FormProvider context instead of passing props
- **Dynamic arrays**: Use useFieldArray instead of manual state management

## 🤖 **AI Assistant Instructions**

### **When Working on Forms**
1. **ALWAYS** check `docs/frontend/REACT_FORM_RESEARCH.md` first
2. **ALWAYS** use FormProvider architecture
3. **ALWAYS** use useFieldArray for dynamic arrays
4. **ALWAYS** use Controller for complex components
5. **ALWAYS** test checkbox functionality (common issue)

### **Code Review Checklist**
- [ ] Uses FormProvider instead of prop drilling
- [ ] Uses useFieldArray for dynamic arrays
- [ ] Uses Controller for complex components
- [ ] Has triggerMode: "onChange" in useForm config
- [ ] Follows 2025 best practices from REACT_FORM_RESEARCH.md

## 📞 **Support**
- Check `docs/frontend/REACT_FORM_RESEARCH.md` for form issues
- Refer to existing components for patterns
- Follow the modern 2025 architecture established in ProfileWizardSteps

---
*Last updated: 2025 - CareerHub Profile Wizard Implementation*