import { Component, ElementRef, OnInit, Renderer2, ViewChild } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})

export class NavbarComponent implements OnInit{
  loginForm!: FormGroup;
  @ViewChild("divVerifyPassword") divVerifyPassword!: ElementRef;
  ifRegister!: Boolean;
  valueVerifyPassword: string = '';
  titleModal!: string;

  constructor(private renderer: Renderer2) { }
  
  ngOnInit(): void {
    this.titleModal = 'Ingresar a NutriPlan'
    this.ifRegister = false;
    this.loginForm = new FormGroup({
      email: new FormControl('', [Validators.required, Validators.email]),
      password: new FormControl('', [Validators.required])
    })
  }
  
  verifyPassword(): boolean{
    return this.loginForm.get('password')?.value === this.valueVerifyPassword
  }

  formRegister(){
    this.titleModal = 'Registrarme en NutriPlan'
    this.ifRegister = true
    this.renderer.removeClass(this.divVerifyPassword.nativeElement, "d-none");
  }

  formLogin(){
    this.titleModal = 'Ingresar a NutriPlan'
    this.ifRegister = false
    this.renderer.addClass(this.divVerifyPassword.nativeElement, "d-none");
  }

  get emailField(): any {
    return this.loginForm.get('email');
  }
  
  get passwordField(): any {
    return this.loginForm.get('password');
  }
  
  limpiarForm(): void {
    this.titleModal = 'Ingresar a NutriPlan'
    this.ifRegister = false
    this.renderer.addClass(this.divVerifyPassword.nativeElement, "d-none");
    this.loginForm.reset()
  }

  loginFormSubmit(): void {
    console.log(this.loginForm.value);
    // Call Api
  }
}
