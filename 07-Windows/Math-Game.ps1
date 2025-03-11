#petite phrase d'accueil qui permetra au joueur de lancer le niveau
$Choix = Read-Host "Vous voici dans un jeu de plus grand ou plus petit, veuillez choisir un niveau de difficulté : 1 = Facile 2 = Moyen 3 = Difficile "
$Essai = 1
#initialisation d'un tableau allant de 1 à 3
$Niveau = 1, 2, 3
#creation d'une boucle qui compare choix et la valeur du tableau du niveau
if($Choix -eq $Niveau[0]){

#parametrage de la valeur du nombre d'essai à 20 en fonction du choix Facile
  $Essai = 20
  Write-Host "Vous avez choisi la difficulté Facile, vous avez $Essai essais ! Bonne chance !  "
}

#parametrage de la valeur du nombre d'essai à 15 en fonction du choix Moyen
elseif($Choix -eq $Niveau[1]){
  $Essai = 15
  Write-Host "Vous avez choisi la difficulté Moyen, vous avez $Essai essais ! Bonne chance ! "
}
#parametrage de la valeur du nombre d'essai à 10 en fonction du choix Difficile
elseif($Choix -eq $Niveau[2]){
  $Essai = 10
  Write-Host "Vous avez choisi la difficulté Difficile, vous avez $Essai essais ! Bonne chance ! "
}


#Declaration des variables maximum et minimum
$minimum = 1
$maximum = 20

#Parametrage d'une variable qui qui déterminera un chiffre a deviner et qui forcera à ce que l'enregistrement soit un integer (plus facile pour les calculs)
[int]$chiffreADeviner = Get-Random -Minimum $minimum -Maximum $maximum
#$chiffreADeviner

#initialisation d'une variable de comparaison qui permettra de définir une limite de de vie à la variable Essai
$Mort = 0

#initialisation d'une boucle qui fait continuera tant que $Essai est différent de $Mort,
while($Essai -ne $Mort){

  #affichage du nombre de vie
   Write-Host "Il vous reste $Essai essais !"

   #decrementation du nombre d'essai
   $Essai --

   #utilisateur choisit un nombre qui sera automatiquement convertit en integer (plus facile pour les calculs)
   [int]$nbUser = Read-Host = "Choisissez un nombre entre 1 et 20"

   #initialisation d'une boucle avec comme 1ere condition un if qui compare l'egalite entre le nombre d'utilisateur et qui si elle est validee finira le jeu par une VICTOIRE !
   if($chiffreADeviner -eq $nbUser){
   Write-Host "GG beau gosse"
   break
 }
 #2eme condition de comparaison si le nombre entré est plus grand que le nombre a trouver
 elseif($nbUser -gt $chiffreADeviner){
   Write-Host "Le chiffre est plus petit"
 }
#3eme condition de comparaison : affiche que le nombre entré est plus petit que le nombre a trouver
 elseif($nbUser -lt $chiffreADeviner){
   Write-Host "Le chiffre est plus Grand ! "
 }
 #gestion des cas non gérés
 else{
   Write-Host "il y a eu une erreur "
 }
 }
